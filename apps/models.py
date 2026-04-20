from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Sotuvchi(models.Model):
    tg_id = models.BigIntegerField(unique=True, null=False)
    fullname = models.CharField(max_length=100, null=False)
    phone1 = models.CharField(max_length=20, unique=True, null=False)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    market_name = models.CharField(max_length=255, unique=True, null=False)
    card_number = models.CharField(max_length=20, null=True, blank=True)
    qr_image = models.ImageField(upload_to='qr_images/', null=True, blank=True)
    market_id = models.IntegerField(
        unique=True,
        null=False,
        validators=[
            MinValueValidator(10000, message="Market ID 5 raqamli bo'lishi kerak"),
            MaxValueValidator(99999, message="Market ID 5 raqamli bo'lishi kerak"),
        ]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.fullname} | {self.market_name}"


class Mijoz(models.Model):
    tg_id = models.BigIntegerField(unique=True, null=False)
    fullname = models.CharField(max_length=100, null=False)
    phone1 = models.CharField(max_length=20, unique=True, null=False)
    phone2 = models.CharField(max_length=20, null=True, blank=True)
    sotuvchilarim = models.ManyToManyField(
        Sotuvchi,
        related_name='mijozlar',
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.fullname} | {self.phone1}"


class Qarzlar(models.Model):
    class Status(models.TextChoices):
        RAD_QILINGAN = 'rad_qilingan', 'Rad qilingan'
        TASDIQLANGAN = 'tasdiqlangan', 'Tasdiqlangan'
        KUTILMOQDA = 'kutilmoqda', 'Kutilmoqda'

    sotuvchi = models.ForeignKey(
        Sotuvchi,
        on_delete=models.CASCADE,
        related_name='qarzlar',
        null=False
    )
    mijoz = models.ForeignKey(
        Mijoz,
        on_delete=models.CASCADE,
        related_name='qarzlar',
        null=False
    )
    qarz_created_at = models.DateTimeField(default=timezone.now)
    pul_miqdori = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(1000, message="Pul miqdori 1000 dan kam bo'lmasligi kerak"),
            MaxValueValidator(3000000, message="Pul miqdori 3,000,000 dan oshmasligi kerak"),
        ]
    )
    qarz_sorov_tg_id = models.BigIntegerField(null=False)
    qarz_tasdiq_tg_id = models.BigIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='qarz_images/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.KUTILMOQDA
    )

    def __str__(self):
        return f"{self.sotuvchi} → {self.mijoz} | {self.pul_miqdori} so'm | {self.get_status_display()}"


class Tolovlar(models.Model):
    sotuvchi = models.ForeignKey(
        Sotuvchi,
        on_delete=models.CASCADE,
        related_name='tolovlar',
        null=False
    )
    mijoz = models.ForeignKey(
        Mijoz,
        on_delete=models.CASCADE,
        related_name='tolovlar',
        null=False
    )
    created_at = models.DateTimeField(default=timezone.now)
    pul_miqdori = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(1000, message="Pul miqdori 1000 dan kam bo'lmasligi kerak"),
            MaxValueValidator(3000000, message="Pul miqdori 3,000,000 dan oshmasligi kerak"),
        ]
    )
    tasdiq_time = models.DateTimeField(null=True, blank=True)
    sotuvchi_tg_id = models.BigIntegerField(null=False)

    def __str__(self):
        return f"{self.sotuvchi} → {self.mijoz} | {self.pul_miqdori} so'm"
    
    