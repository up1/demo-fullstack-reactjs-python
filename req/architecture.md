# Tracking status of Order

## Architecture
The system will be designed to allow users to track the status of their orders using a 13 digit item number. The architecture will consist of the following components:
1. User Interface: A web-based interface where users can input their item numbers and view the tracking status of their orders.
2. Backend Server: A server that processes the user input, retrieves the tracking information from the database, and sends the response back to the user interface.
3. Database: A database that stores the tracking information for all orders. This database will be updated regularly to ensure that the tracking information is accurate and up-to-date.

## Non-Functional Requirements
1. Performance: The system should be able to handle a large number of requests simultaneously without significant delays in response time.
2. Scalability: The system should be designed to accommodate future growth in the number of users and orders without requiring significant changes to the architecture.
3. Security: The system should implement appropriate security measures to protect user data and prevent unauthorized access to the tracking information.
4. Usability: The user interface should be intuitive and easy to use, allowing users to quickly and easily track their orders without confusion or frustration.

## Features
Enter the 13 digit item number [Sample : EF582568151TH]

Search
* Please enter , (Comma) Item number separator in the case of more than 1 tracking

(Sample : EF582621151TH, EA666458151TH, RG453678925TH) A maximum of 10 items can be entered at a time

## Technical Stack
1. Frontend: The user interface will be built using React.js for a responsive and dynamic user experience.
2. Backend: The backend server will be developed using Python and FastAPI for efficient handling of requests and responses.
3. Database: PostgreSQL will be used as the database to store tracking information, ensuring data integrity and scalability.
4. Manage container with docker and docker-compose for easy deployment and scalability of the application.
5. API Gateway: Nginx will be used as an API gateway to manage and route incoming requests to the appropriate backend services.


## Project structure with single repository
```.
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   └── crud.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── TrackingForm.js
│   │   │   └── TrackingResults.js
│   │   ├── App.js      
│   │   └── index.js
│   ├── Dockerfile
│   └── package.json
├── api-gateway
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

This architecture allows for a clear separation of concerns between the frontend and backend components, while also ensuring that the system is scalable and maintainable. The use of Docker and Docker Compose will facilitate easy deployment and management of the application across different environments.

## API Endpoints
1. `POST /track`: This endpoint will accept a list of item numbers and return the tracking status for each item. The request body will contain a JSON object with an array of item numbers, and the response will include the tracking status for each item in a structured format. 
2. `GET /track/{item_number}`: This endpoint will allow users to retrieve the tracking status for a specific item number. The item number will be passed as a path parameter, and the response will include the tracking status for that item.
3. `GET /track/batch`: This endpoint will allow users to retrieve the tracking status for multiple item numbers in a single request. The item numbers will be passed as query parameters, and the response will include the tracking status for each item in a structured format.
