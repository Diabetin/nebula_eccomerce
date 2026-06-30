from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

#Modelo de Categoria
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


#Modelo de producto usando ORM para definir las relaciones de productos y categorias
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]) #Se agrega un validador para que el precio no sea negativo
    stock = models.PositiveIntegerField(null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products') #ForeignKey para relacionar productos con categorias, on_delete=models.SET_NULL para que si se elimina una categoria, los productos asociados no se eliminen, sino que su campo category se establezca en NULL. null=True y blank=True permiten que el campo category sea opcional. related_name='products' permite acceder a los productos de una categoria desde la instancia de la categoria.
    image = models.ImageField(upload_to='product_images/', null=True, blank=True) #Se agrega un campo de imagen para el producto, upload_to especifica la carpeta donde se guardarán las imágenes, null=True y blank=True permiten que el campo image sea opcional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Modelo para el carrito de compras con detalles de los productos agregados al carrito
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    products = models.ManyToManyField(Product, through='CartItem') #ManyToManyField para relacionar el carrito con los productos, a través del modelo intermedio CartItem
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"
    
# Modelo intermedio para representar los productos en el carrito de compras, con la cantidad de cada producto
class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) #ForeignKey para relacionar el item del carrito con el carrito, on_delete=models.CASCADE para que si se elimina un carrito, los items asociados también se eliminen
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #ForeignKey para relacionar el item del carrito con el producto, on_delete=models.CASCADE para que si se elimina un producto, los items asociados también se eliminen
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)]) #Se agrega un validador para que la cantidad no sea menor a 1
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

# Modelo para ordenes de compra, con detalle de productos, cantidad y precio total de usuarios que no son staff
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) #ForeignKey para relacionar la orden con el usuario, on_delete=models.CASCADE para que si se elimina un usuario, las ordenes asociadas también se eliminen
    products = models.ManyToManyField(Product, through='OrderItem') #ManyToManyField para relacionar la orden con los productos, a través del modelo intermedio OrderItem
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]) #Se agrega un validador para que el precio total no sea negativo
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model): # Modelo intermedio para representar los productos en la orden de compra, con la cantidad de cada producto y el precio total
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.id} - {self.product.name}"