1.	Open Postman and create a new request.
2.	Set the request method to POST.
3.	Enter the request URL for your Django API endpoint where you want to add the new vendor. For example: http://localhost:8000/api/vendors/.
4.	Go to the Headers section and add a new header with key Content-Type and value application/json. This header tells the server that the request body will be in JSON format.
5.	Switch to the Body tab.
6.	Select the raw option and choose JSON (application/json) from the dropdown menu.

{
    "name": "KVV Timbers",
    "contact_details": "1234567890, kvv@gmail.com",
    "address": "Main ROAd, Batlagundu"
}



GET http://localhost:8000/api/vendors/

It Lists all vendors

GET http://localhost:8000/api/vendors/ {vendor_id}/
Retrieve a specific vendor's details.

PUT  http://localhost:8000/api/vendors/ {vendor_id}/

{
    "name": "Kannan Timbers",
    "contact_details": "9843027787, Kannandear@gmail.com",
    "address": "Noida"
}

Body should be like this.
1.	Headers section and add a new header with key Content-Type and value application/json. This header tells the server that the request body will be in JSON format.

DELETE  http://localhost:8000/api/vendors/ {vendor_id}/

Delete a vendor.
 
Purchase Order

POST http://localhost:8000/api/purchase_orders/

Headers 
"Content-Type" = "application/json"
Json body format

{
    "vendor": 14,
    "order_date": "2024-04-12T09:00:00",
    "delivery_date": "2024-04-19T18:00:00",
    "items": [
        {
            "item_name": "Item 1",
            "quantity": 10
        },
        {
            "item_name": "Item 2",
            "quantity": 5
        }
    ],
    "quantity": 15,
    "status": "pending",
    "issue_date": "2024-04-13T09:05:00"
}

 
GET  http://localhost:8000/api/purchase_orders/

Headers 
"Content-Type" = "application/json"
It lists all Purchase orders


GET  http://localhost:8000/api/purchase_orders/ {po_id}/
"Content-Type" = "application/json"
It list Particular PO id
PUT  http://localhost:8000/api/purchase_orders/ {po_id}/
"Content-Type" = "application/json"
Json body format is 

{
    "id": 13,
    "po_number": "a95c2f84-2",
    "order_date": "2024-04-13T09:00:00Z",
    "delivery_date": "2024-04-19T18:00:00Z",
    "items": [
        {
            "item_name": "Item 1",
            "quantity": 10
        },
        {
            "item_name": "Item 2",
            "quantity": 5
        }
    ],
    "quantity": 15,
    "status": "completed",
    "quality_rating": 3.5,
    "issue_date": "2024-04-13T09:05:00Z",
    "acknowledgment_date": null,
    "vendor": 13
}

Delete  http://localhost:8000/api/purchase_orders/ {po_id}/

It deletes the partucular PO


POST http://localhost:8000/api/purchase_orders/ {po_id}/acknowledge/

"Content-Type" = "application/json"
Json body format is 

{
    "acknowledgment_date": "2024-04-14T09:05:00Z"
}
 
Vendor Performance

GET http://localhost:8000/api/vendors/ {vendor_id}/performance
 



