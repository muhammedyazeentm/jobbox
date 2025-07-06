from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, WorkerProfile, ShopOrIndividualProfile

WORKER_SKILLS = [
    ('Accountant', 'Accountant'),
    ('Baby Sitter', 'Baby Sitter'),
    ('Beautician', 'Beautician'),
    ('Cleaner', 'Cleaner'),
    ('Construction Worker', 'Construction Worker'),
    ('Cook/Chef', 'Cook/Chef'),
    ('Driver', 'Driver'),
    ('Electrician', 'Electrician'),
    ('Farmer', 'Farmer'),
    ('Gardener', 'Gardener'),
    ('Maintenance Worker', 'Maintenance Worker'),
    ('Maidservant', 'Maidservant'),
    ('Mason', 'Mason'),
    ('Mechanic', 'Mechanic'),
    ('Pharmacist', 'Pharmacist'),
    ('Photographer', 'Photographer'),
    ('Salesman', 'Salesman'),
    ('Security Guard', 'Security Guard'),
    ('Tailor', 'Tailor'),
    ('Waiter', 'Waiter'),
    ('Other skilled worker', 'Other skilled worker'),
]

SHOP_CATEGORIES = [
    ('Automobile/Workshop', 'Automobile/Workshop'),
    ('Accessories', 'Accessories'),
    ('Agriculture', 'Agriculture'),
    ('Beauty/Hair', 'Beauty/Hair'),
    ('Clothing/Textiles', 'Clothing/Textiles'),
    ('Construction', 'Construction'),
    ('Electrical/Electronics', 'Electrical/Electronics'),
    ('Food/Beverages', 'Food/Beverages'),
    ('Grocery', 'Grocery'),
    ('Hotel/Restaurants', 'Hotel/Restaurants'),
    ('Industrial', 'Industrial'),
    ('Jewellery', 'Jewellery'),
    ('Medical', 'Medical'),
    ('Photography/Studio', 'Photography/Studio'),
    ('Private Business/Properties', 'Private Business/Properties'),
    ('Repair/Maintenance', 'Repair/Maintenance'),
    ('Service Related', 'Service Related'),
    ('Other', 'Other'),
]

KERALA_CITIES = [
    ('Alappuzha', 'Alappuzha'),
    ('Adoor', 'Adoor'),
    ('Aluva', 'Aluva'),
    ('Angamaly', 'Angamaly'),
    ('Attingal', 'Attingal'),
    ('Chalakudy', 'Chalakudy'),
    ('Changanassery', 'Changanassery'),
    ('Cherthala', 'Cherthala'),
    ('Ernakulam', 'Ernakulam'),
    ('Guruvayur', 'Guruvayur'),
    ('Idukki', 'Idukki'),
    ('Kannur', 'Kannur'),
    ('Kasaragod', 'Kasaragod'),
    ('Kayamkulam', 'Kayamkulam'),
    ('Kochi', 'Kochi'),
    ('Kodungallur', 'Kodungallur'),
    ('Kollam', 'Kollam'),
    ('Kothamangalam', 'Kothamangalam'),
    ('Kottayam', 'Kottayam'),
    ('Kozhikode', 'Kozhikode'),
    ('Malappuram', 'Malappuram'),
    ('Mavelikkara', 'Mavelikkara'),
    ('Muvattupuzha', 'Muvattupuzha'),
    ('Nedumangad', 'Nedumangad'),
    ('Neyyattinkara', 'Neyyattinkara'),
    ('Ottapalam', 'Ottapalam'),
    ('Palai', 'Palai'),
    ('Palakkad', 'Palakkad'),
    ('Pathanamthitta', 'Pathanamthitta'),
    ('Pattambi', 'Pattambi'),
    ('Pattimattom', 'Pattimattom'),
    ('Perinthalmanna', 'Perinthalmanna'),
    ('Ponnani', 'Ponnani'),
    ('Shoranur', 'Shoranur'),
    ('Thalassery', 'Thalassery'),
    ('Thiruvalla', 'Thiruvalla'),
    ('Thiruvananthapuram', 'Thiruvananthapuram'),
    ('Thodupuzha', 'Thodupuzha'),
    ('Thrissur', 'Thrissur'),
    ('Tirur', 'Tirur'),
    ('Vadakara', 'Vadakara'),
    ('Varkala', 'Varkala'),
    ('Other', 'Other'),
]


class ShopIndividualSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), required=True)
    password1 = forms.CharField(label="Create Password", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), help_text='')
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), help_text='')
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, widget=forms.RadioSelect)
    location = forms.ChoiceField(choices=[('', 'Select your city')] + KERALA_CITIES, widget=forms.Select(attrs={'class': 'form-control'}))
    shop_name = forms.CharField(required=False)
    owner_name = forms.CharField(required=False)
    category = forms.ChoiceField(choices=[('', 'Select Category')] + SHOP_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    description = forms.CharField(required=False, widget=forms.Textarea)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['user_type', 'username', 'email', 'shop_name', 'category', 'description', 'owner_name',
                  'contact_number', 'location', 'profile_picture', 'password1', 'password2']
        help_texts = {
            'username': '',
        }

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")

        if user_type == "shop":
            if not cleaned_data.get("shop_name"):
                self.add_error("shop_name", "Shop Name is required for shops.")
            if not cleaned_data.get("owner_name"):
                self.add_error("owner_name", "Owner Name is required for shops.")
            if not cleaned_data.get("category"):
                self.add_error("category", "Category is required for shops.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile_picture = self.cleaned_data.get('profile_picture')

        if commit:
            user.save()

            user_type = self.cleaned_data.get('user_type')
            profile_picture = self.cleaned_data.get('profile_picture')

            if user_type == "shop":
                ShopOrIndividualProfile.objects.create(
                    user=user,
                    user_type='shop',
                    shop_name=self.cleaned_data.get('shop_name'),
                    category=self.cleaned_data.get('category'),
                    description=self.cleaned_data.get('description'),
                    owner_name=self.cleaned_data.get('owner_name'),
                    contact_number=self.cleaned_data.get('contact_number'),
                    location=self.cleaned_data.get('location'),
                    profile_picture=profile_picture
                )
            elif user_type == "individual":
                ShopOrIndividualProfile.objects.create(
                    user=user,
                    user_type='individual',
                    Name=self.cleaned_data.get('username'),
                    contact_number=self.cleaned_data.get('contact_number'),
                    location=self.cleaned_data.get('location'),
                    profile_picture=profile_picture
                )
        return user


class WorkerSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), required=True)
    password1 = forms.CharField(label="Create Password", widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), help_text='')
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), help_text='')
    Name = forms.CharField(required=False)
    Other_skills = forms.CharField(required=True, widget=forms.Textarea)
    experience_in_years = forms.IntegerField(required=False, min_value=1, max_value=10)
    profile_picture = forms.ImageField(required=False)
    location = forms.ChoiceField(choices=[('', 'Select your city')] + KERALA_CITIES, widget=forms.Select(attrs={'class': 'form-control'}))
    I_am_a = forms.ChoiceField(choices=[('', 'Select your work')] + WORKER_SKILLS, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'Name', 'I_am_a', 'contact_number', 'location', 'password1', 'password2',
                  'Other_skills', 'experience_in_years', 'profile_picture']
        help_texts = {
            'username': '',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile_picture = self.cleaned_data.get('profile_picture')

        if commit:
            user.save()

            WorkerProfile.objects.create(
                user=user,
                Name=self.cleaned_data.get('username'),
                I_am_a=self.cleaned_data.get('I_am_a'),
                contact_number=self.cleaned_data.get('contact_number'),
                location=self.cleaned_data.get('location'),
                experience_in_years=self.cleaned_data.get('experience_in_years'),
                Other_skills=self.cleaned_data.get('Other_skills'),
                profile_picture=self.cleaned_data.get('profile_picture')
            )
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username', 'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password','autocomplete': 'new-password'}))

class ShopProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(required=True)
    owner_name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    shop_name = forms.CharField(required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = ShopOrIndividualProfile
        fields = ['shop_name', 'owner_name', 'contact_number', 'description', 'profile_picture']
class IndividualProfileEditForm(forms.ModelForm):
    email = forms.EmailField()
    contact_number = forms.CharField(max_length=15)
    Name = forms.CharField(max_length=100)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = ShopOrIndividualProfile
        fields = ['email', 'contact_number', 'Name', 'profile_picture']

class WorkerProfileEditForm(forms.ModelForm):
    Name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")
    contact_number = forms.CharField(label="Contact Number")
    experience_in_years = forms.IntegerField(label="Experience (in years)")
    profile_picture = forms.ImageField(label="Profile Picture", required=False)

    class Meta:
        model = WorkerProfile
        fields = ['Name', 'email', 'contact_number', 'experience_in_years', 'profile_picture']
