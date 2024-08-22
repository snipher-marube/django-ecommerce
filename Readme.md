# Django Ecommerce

This is a fully functional ecommerce website built with Django and Tailwind CSS.

## Features

- Account Registration: Users can create an account to access additional features.
- Product Catalog: Display a list of products with details such as name, price, and description.
- Shopping Cart: Users can add products to their cart and proceed to checkout.
- Order Management: Admins can manage orders, view order details, and update order status.
- Payment Integration: Integration with a payment gateway to process payments securely.
- User Authentication: Secure user authentication and authorization for protected areas of the site.
- Product Search: Users can search for products by name or category.
- Product Reviews: Users can leave reviews and ratings for products.
- Order History: Users can view their order history and track the status of their orders.
- Responsive Design: The website is optimized for different screen sizes and devices.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/snipher-marube/django-ecommerce.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the development server:

    ```bash
    export DJANGO_SETTINGS_MODULE=DjangoEcommerce.settings.development
    python manage.py runserver
    ```

4. Set up the database:

    ```bash
    python manage.py migrate
    ```

5. Open your browser and visit `http://localhost:8000` to access the website.

## Setting up Django-allauth with Google

1. Go to the [Google Developer Console](https://console.developers.google.com/) and create a new project.

2. Enable the Google+ API for your project:
   - In the sidebar, click on "Library".
   - Search for "Google+ API" and click on it.
   - Click on the "Enable" button.

3. Create OAuth 2.0 credentials:
   - In the sidebar, click on "Credentials".
   - Click on the "Create Credentials" button and select "OAuth client ID".
   - Select "Web application" as the application type.
   - Enter a name for your credentials.
   - Under "Authorized JavaScript origins", add `http://localhost:8000` (replace with your actual domain if needed).
   - Under "Authorized redirect URIs", add `http://localhost:8000/accounts/google/login/callback/` (replace with your actual domain if needed).
   - Click on the "Create" button.

4. Copy the generated "Client ID" and "Client Secret" values.

5. Navigate to you admin panel then under add social application add Client ID and Client Secret and Name.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
