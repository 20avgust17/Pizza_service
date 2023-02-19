Build the images and run the containers:

$ docker-compose up -d --build


This pizza service project aims to provide a seamless experience for customers who want to order their favorite pizza online. The project will use Python, FastAPI, SQLAlchemy, Pydantic, Alembic, Celery, Redis, FastAPI-Users, Flower, PostgreSQL as the primary technologies.

The project will have a storefront where customers can browse through a variety of pizzas, select their favorite toppings, and place an order. Customers can also create an account, which will save their preferences and previous orders, making future purchases easier.The project will also feature a blog section, which will provide customers with the latest news and updates about the pizza service. 

FastAPI will be used to develop the backend of the project, with SQLAlchemy and Pydantic as the primary tools for managing the database and data validation. Alembic will be used for database migrations, which allows for seamless updates to the database schema without causing data loss.

Celery and Redis will be used to handle background tasks and improve the performance of the project and cache. Flower will provide monitoring and visualization for the Celery tasks. FastAPI-Users will be used to manage user authentication and authorization.

The project will use PostgreSQL as the database, providing reliable data storage and retrieval. The use of async will be prioritized throughout the project to ensure quick and efficient execution.

Overall, this pizza service project will offer customers an easy and convenient way to order their favorite pizzas, while also providing valuable information and updates through the blog section. The use of Python, FastAPI, and other modern technologies will ensure that the project is fast, reliable, and easy to use.
