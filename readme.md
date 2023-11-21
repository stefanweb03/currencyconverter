
# Currency Converter Application

## Main Goal
Develop a robust REST API application for currency conversion. This application aims to provide real-time currency exchange information and conversion services, ensuring accurate and up-to-date financial data exchange.

## Key Technologies

- **Spring Boot**: A cornerstone for building a scalable and efficient backend. It streamlines the development process and offers a robust framework for API request handling.
- **PostgreSQL**: Our chosen database management system, ideal for storing historical exchange rates and user data. Known for its reliability and efficient data retrieval capabilities.
- **Postman**: A crucial tool for API testing, ensuring that all endpoints are responsive and handle various HTTP requests as expected.
- **React**: The technology behind our frontend development. React's versatility makes it an excellent choice for crafting dynamic and responsive user interfaces.

## Development Process

1. **Backend Setup (Spring Boot and PostgreSQL)**: Setting up the server, defining data models, and integrating with the PostgreSQL database to manage currency data and user preferences.
2. **Database Design and Schema**: Crafting a schema to efficiently store currency exchange rates, user queries, and other pertinent data.
3. **Implementing RESTful Endpoints**: Developing endpoints for currency conversion, accessing current and historical exchange rates, and managing user accounts.
4. **Testing with Postman**: Conducting thorough testing of each endpoint to ensure precise data handling and responses.
5. **Frontend Development (React)**: Creating user interfaces for currency conversion, exchange rate viewing, and user account management.
6. **Integration of Frontend and Backend**: Seamlessly connecting the user interface with the server to provide a fluid user experience.

## Benefits

- **Real-time Data Access**: Offering users the most current currency exchange rates.
- **User-friendly Interface**: The React frontend delivers an intuitive and responsive experience.
- **Reliable Data Storage**: PostgreSQL guarantees the integrity and availability of historical exchange rate data.
- **Comprehensive Testing**: Ensuring the reliability and precision of our currency conversion service.

## Entities

- **Java Classes**: Creating entities like Currency, ExchangeRate, and UserAccount.
- **Repositories**: Implementing Spring Data JPA repositories for entities such as CurrencyRepository and ExchangeRateRepository.
- **Service Layer**: Developing services like CurrencyService and UserService for business logic.
- **Controller Layer**: Establishing controllers like CurrencyController and UserController with methods for API endpoints.
- **Request and Response DTOs**: Defining DTOs for efficient data transfer in API requests and responses.
- **Exception Handling**: Implementing both global and controller-specific exception handling.
- **Security**: Utilizing Spring Security for authentication and authorization, potentially integrating OAuth2 for user accounts.
- **Documentation**: Incorporating Swagger for comprehensive API documentation.
- **Dependency Management**: Employing Maven or Gradle for dependency management.
- **Configuration**: Setting up application properties and database configurations in line with Spring Boot standards.

## Swagger Sample Code

Defining OpenAPI specifications for endpoints like `/convert`, `/rates`, `/user/login`, etc.

```yaml

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

```

## Elasticsearch Mapping

```json
{
  "mappings": {
    "properties": {
      "currencyCode": {
        "type": "keyword"  // Ideal for exact matches, crucial for currency codes
      },
      "rate": {
        "type": "double"  // Perfect for storing exchange rates with precision
      },
      "timestamp": {
        "type": "date",  // Date type for timestamp, customizable format
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
```

### Detailed Explanation of Elasticsearch Mapping

- **Field: `currencyCode`**
  - **Type:** `keyword`
  - **Description:** Optimized for exact match queries, essential for identifying specific currency codes.
- **Field: `rate`**
  - **Type:** `double`
  - **Description:** Designed to store exchange rates with decimal precision.
- **Field: `timestamp`**
  - **Type:** `date`
  - **Description:** Customizable to match the application's date format, ensuring consistency in date representations.
- **Field: `historicalRates`**
  - **Type:** `nested`
  - **Description:** Ideal for storing complex objects like historical exchange rate data, with sub-fields for date and rate.

This documentation is crafted to provide a comprehensive overview of the Currency Converter Application, detailing its goals, technologies, development process, and the intricacies of its Elasticsearch mapping.

Type: nested
Description: The historicalRates field is categorized as a nested type. This structure is particularly useful for storing complex objects, such as historical exchange rate data. Within each historicalRates object, there are sub-fields for date (of date type) and rate (of double type). This nested arrangement allows for efficient organization and retrieval of historical rate information for each currency.
