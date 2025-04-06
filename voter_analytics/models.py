from django.db import models
import csv
import os
from datetime import datetime
from django.conf import settings


# Create your models here.
class Voter(models.Model):
    voter_id = models.CharField(max_length=12, primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    registration_date = models.DateField()
    party_affiliation = models.CharField(max_length=3)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.voter_id})"

def load_data(file_path):
    count = 0
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            count += 1
            if count % 100 == 0:
                print(f"Processing record {count}...")
            
            # Convert string 'TRUE'/'FALSE' to boolean
            v20state = row['v20state'] == 'TRUE'
            v21town = row['v21town'] == 'TRUE'
            v21primary = row['v21primary'] == 'TRUE'
            v22general = row['v22general'] == 'TRUE'
            v23town = row['v23town'] == 'TRUE'
            
            # Parse dates
            date_of_birth = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
            registration_date = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()
            
            # Create voter instance
            voter = Voter(
                voter_id=row['Voter ID Number'],
                last_name=row['Last Name'],
                first_name=row['First Name'],
                street_number=row['Residential Address - Street Number'],
                street_name=row['Residential Address - Street Name'],
                apartment_number=row['Residential Address - Apartment Number'],
                zip_code=row['Residential Address - Zip Code'],
                date_of_birth=date_of_birth,
                registration_date=registration_date,
                party_affiliation=row['Party Affiliation'].strip(),  # Strip whitespace
                precinct_number=row['Precinct Number'].strip(),  # Use as string, strip whitespace
                v20state=v20state,
                v21town=v21town,
                v21primary=v21primary,
                v22general=v22general,
                v23town=v23town,
                voter_score=int(row['voter_score'])
            )
            voter.save()
    print(f"Imported {count} records successfully.")
