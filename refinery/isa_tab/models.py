from django.db import models

# Create your models here.
class Investigation(models.Model):
    def __unicode__(self):
        return self.accession

    accession = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=2048)

class Investigator(models.Model):
    def __unicode__(self):
        name = "%s, %s" % (self.last_name, self.first_name)
        return name

    email = models.EmailField(max_length=255, primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    mid_initial = models.CharField(max_length=1, blank=True)
    affiliation = models.CharField(max_length=50)
    investigation = models.ManyToManyField(Investigation)

class Sub_Type(models.Model):
    def __unicode__(self):
        return self.type

    type = models.CharField(max_length=30, primary_key=True)
    
class Raw_Data(models.Model):
    def __unicode__(self):
        return self.file_name

    file_name = models.CharField(max_length=255)
    url = models.CharField(max_length=2048)

class Processed_Data(models.Model):
    def __unicode__(self):
        return self.file_name

    file_name = models.CharField(max_length=255)
    url = models.CharField(max_length=2048)
    
class Assay(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    raw_data = models.ManyToManyField(Raw_Data)
    processed_data = models.ManyToManyField(Processed_Data, blank=True)
    investigation = models.ForeignKey(Investigation)

class Characteristic(models.Model):
    def __unicode__(self):
        return self.type

    value = models.CharField(max_length=20)
    type = models.ForeignKey(Sub_Type)
    assay = models.ForeignKey(Assay)

class Factor_Value(models.Model):
    def __unicode__(self):
        return self.type

    value = models.CharField(max_length=20)
    type = models.ForeignKey(Sub_Type)
    assay = models.ForeignKey(Assay)
