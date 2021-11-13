// 	Querying for all elements with class set to update-cart
var updateBtns = document.getElementsByClassName('update-cart')
for (let query of updateBtns) {
	//listening on click
	query.addEventListener('click', function() {
		let productId = query.dataset.product
		let action = query.dataset.action
		console.log(`Product: ${productId} action: ${action}`)
		console.log(user)
		// user inherited from main.html  user = request.user
		if (user == 'AnonymousUser') {
			addCookieItem(productId, action)
	}
		else {
			updateUserOrder(productId, action)
			// Reloading page when new data is sent through
			location.reload()
	}
	})
	
}

function addCookieItem(productId, action){
	console.log('Not logged in...')
	if (action == 'add') {
		// Creating quantity of 1 if cart is empty for any product
		if (cart[productId] == null){
			cart[productId] = {'quantity': 1}
		}
		else {
			cart[productId]['quantity'] += 1
		}	
	}
	if (action == 'remove') {
		cart[productId]['quantity'] -= 1
		// Deleting object if value of quantity is less than or equal to zero
		if (cart[productId]['quantity'] <= 0){
			delete cart[productId]
		}
	}
	console.log(cart)
	// Updating cookie  
	document.cookie = 'cart=' + JSON.stringify(cart) +'; domain=;path=/'
	location.reload()
}

function updateUserOrder(productId, action) {
	console.log("User is logged in, Sending data now..")
	// Url to send the data to
	var url = '/update/'

	fetch(url, {
		method:'POST' ,
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		// parsing the javascript object to json 
		body: JSON.stringify({'productId':productId, 'action':action})
	})
	// Asking for the json response from the updateItem_view
	.then(response => {
		return response.json()
	})
	// data has been received from that view now consoling out the data
	.then((data) => {
		console.log(data)
		location.reload()
	}) 
}