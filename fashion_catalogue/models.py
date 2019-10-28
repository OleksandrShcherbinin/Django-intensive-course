from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=20)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)
    objects = models.Manager()

    def __str__(self):
        return self.name


class FashionItem(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    img = models.ImageField(upload_to='images')
    image_url = models.URLField(null=True, blank=True)
    size = models.ManyToManyField(Size)
    color = models.ManyToManyField(Color)
    price = models.FloatField()
    item_source = models.URLField(null=True, blank=True)
    parsing_date = models.DateTimeField(auto_created=True, null=True, blank=True)

    cat = models.ManyToManyField(Category)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Reviews(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField()
    rates = [(i, i) for i in range(1, 6)]
    rating = models.IntegerField(default=5, choices=rates)
    comment = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)

    fashion_item = models.ForeignKey(FashionItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

