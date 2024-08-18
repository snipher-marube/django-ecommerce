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

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
