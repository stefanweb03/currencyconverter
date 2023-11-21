**Currency Converter Application**

Main Goal:
Develop a robust REST API application for currency conversion. This application will facilitate real-time currency exchange information and conversion services, ensuring accurate and up-to-date financial data exchange.

Key Technologies:

Spring Boot: Utilized for building a scalable and efficient backend. It simplifies the development process and provides a robust framework for handling API requests.

PostgreSQL: Chosen as the database management system for storing historical exchange rates and user data. PostgreSQL offers reliability and efficient data retrieval.

Postman: Essential for testing the API, ensuring that all endpoints respond correctly and handle various HTTP requests as expected.

React: Employed for the frontend development. React is a versatile framework for building dynamic and responsive user interfaces.

Development Process:

Backend Setup (Spring Boot and PostgreSQL): Establish the server, define data models, and connect to the PostgreSQL database to manage currency data and user preferences.

Database Design and Schema: Design a schema to efficiently store currency exchange rates, user queries, and other relevant data.

Implementing RESTful Endpoints: Create endpoints for currency conversion, retrieving current and historical exchange rates, and user account management.

Testing with Postman: Rigorously test each endpoint to ensure accurate data handling and response.

Frontend Development (React): Develop user interfaces for currency conversion, viewing exchange rates, and managing user accounts.

Integration of Frontend and Backend: Ensure seamless interaction between the user interface and the server for a smooth user experience.

Benefits:

Real-time Data Access: Provides users with the latest currency exchange rates.
User-friendly Interface: Angular frontend offers an intuitive and responsive user experience.
Reliable Data Storage: PostgreSQL ensures the integrity and availability of historical exchange rate data.
Comprehensive Testing: Ensures the reliability and accuracy of the currency conversion service.
SECOND PART

Entities:

Create Java classes for entities like Currency, ExchangeRate, and UserAccount.
Repositories:

Implement Spring Data JPA repositories for each entity, such as CurrencyRepository and ExchangeRateRepository.
Service Layer:

Develop services like CurrencyService and UserService for business logic.
Controller Layer:

Create controllers like CurrencyController and UserController with methods for API endpoints.
Request and Response DTOs:

Define DTOs for handling data transfer in API requests and responses.
Exception Handling:

Implement global and controller-specific exception handling.
Security:

Use Spring Security for authentication and authorization, possibly with OAuth2 for user accounts.
Documentation:

Integrate Swagger for API documentation.
Dependency Management:

Use Maven or Gradle for managing dependencies.
Configuration:

Set up application properties and database configurations according to Spring Boot standards.
SWAGGER SAMPLE CODE

Define OpenAPI specifications for endpoints like /convert, /rates, /user/login, etc.
ElasticSearch Mapping:

I Create mappings for entities like Currency and ExchangeRate with properties such as code, rate, timestamp.

openapi: 3.0.0
info:
  title: Currency Converter API
  description: API for converting currencies and retrieving exchange rates
  version: 1.0.0

paths:
  /convert:
    post:
      summary: Convert currency
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                fromCurrency:
                  type: string
                  description: Currency code to convert from
                toCurrency:
                  type: string
                  description: Currency code to convert to
                amount:
                  type: number
                  format: double
                  description: Amount to be converted
      responses:
        '200':
          description: Conversion successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  convertedAmount:
                    type: number
                    format: double
        '400':
          description: Bad request

  /rates/{currencyCode}:
    get:
      summary: Get current exchange rate for a currency
      parameters:
        - in: path
          name: currencyCode
          required: true
          description: Currency code to get the exchange rate for
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  currencyCode:
                    type: string
                  rate:
                    type: number
                    format: double
        '404':
          description: Currency not found

  /historical-rates:
    get:
      summary: Get historical exchange rates
      parameters:
        - in: query
          name: startDate
          required: true
          description: Start date for historical rates (YYYY-MM-DD)
          schema:
            type: string
            format: date
        - in: query
          name: endDate
          required: true
          description: End date for historical rates (YYYY-MM-DD)
          schema:
            type: string
            format: date
        - in: query
          name: currencyCode
          required: true
          description: Currency code to get historical rates for
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    date:
                      type: string
                      format: date
                    rate:
                      type: number
                      format: double
        '400':
          description: Bad request
        '404':
          description: Currency not found

components:
  schemas:
    Currency:
      type: object
      properties:
        code:
          type: string
        name:
          type: string
        symbol:
          type: string

    ExchangeRate:
      type: object
      properties:
        currencyCode:
          type: string
        rate:
          type: number
          format: double
        timestamp:
          type: string
          format: date-time



**Elasticsearch Mapping**

{
  "mappings": {
    "properties": {
      "currencyCode": {
        "type": "keyword"  // Use 'keyword' for exact matches, important for currency codes
      },
      "rate": {
        "type": "double"  // Suitable for storing exchange rates with precision
      },
      "timestamp": {
        "type": "date",  // Date type for timestamp, with custom format if needed
        "format": "strict_date_optional_time||epoch_millis"
      },
      "historicalRates": {
        "type": "nested",  // Nested type for historical rates
        "properties": {
          "date": {
            "type": "date",
            "format": "yyyy-MM-dd"
          },
          "rate": {
            "type": "double"
          }
        }
      }
    }
  }
}


The Elasticsearch mapping for the currency converter application is designed to optimize data storage and retrieval processes. This mapping defines the data types and structures for various fields relevant to currency conversion. Below is a detailed explanation of each field in the mapping:

Field: currencyCode

Type: keyword
Description: The currencyCode field is defined as a keyword type. This choice is particularly suitable for scenarios requiring exact match queries. For instance, when a user needs to retrieve data for a specific currency code, the keyword type ensures precise and efficient querying.
Field: rate

Type: double
Description: The rate field is set as a double. This data type is essential for representing exchange rates, as it accommodates decimal values. The use of double ensures that the exchange rates are stored with the necessary precision.
Field: timestamp

Type: date
Description: The timestamp field is of the date type. This field can be formatted to align with the specific date format utilized within the application. The flexibility in formatting is crucial for maintaining consistency in date representations across different data entries.
Field: historicalRates

Type: nested
Description: The historicalRates field is categorized as a nested type. This structure is particularly useful for storing complex objects, such as historical exchange rate data. Within each historicalRates object, there are sub-fields for date (of date type) and rate (of double type). This nested arrangement allows for efficient organization and retrieval of historical rate information for each currency.
