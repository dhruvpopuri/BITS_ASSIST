from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
from django.core.files import File

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	bio = models.CharField(max_length=200,default="Hey there!I'm using BITS-Assist")
	image = models.ImageField(upload_to='prof_pics')
	image_url = models.URLField(null=True)
	email = models.EmailField(null=True)

	

	def get_remote_image(self):
		if self.image_url and not self.image:

			result = urllib.urlretrieve(self.image_url)
			self.image.save(
        		os.path.basename(self.image_url),
        		File(open(result[0]))
        		)
			self.save()
	


	if image is not None:	
		def save(self):
			super().save()
			img = Image.open(self.image.path)

			if img.height > 300 or img.width > 300:
				output_size = (300, 300)
				img.thumbnail(output_size)
				img.save(self.image.path)


	def __str__(self):
		return self.user.username



	

