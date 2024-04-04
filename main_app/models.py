from django.db import models

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Jewelry(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField ()
    
    def __str__(self):
      return self.name   

 # Add new Feeding model below Jewelry model
class Feeding(models.Model):
  date = models.DateField('Feeding Date')
  date = models.DateField()
  meal = models.CharField(max_length=1)
  meal = models.CharField(max_length=1, choices=MEALS, default=MEALS[0][0])
  jewelry = models.ForeignKey(Jewelry, on_delete=models.CASCADE)

  def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
    ordering = ['-date']
     
