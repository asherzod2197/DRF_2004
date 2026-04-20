from rest_framework import serializers
from .models import Sotuvchi, Mijoz, Qarzlar, Tolovlar


# ───────────────────────────── SOTUVCHI ─────────────────────────────

class SotuvchiCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sotuvchi
        fields = [
            'tg_id', 'fullname', 'phone1', 'phone2',
            'market_name', 'card_number', 'qr_image', 'market_id',
        ]     


class SotuvchiListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sotuvchi
        fields = ['id', 'tg_id', 'fullname', 'phone1', 'market_name', 'market_id', 'created_at']


class SotuvchiDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sotuvchi
        fields = '__all__'


class SotuvchiUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sotuvchi
        fields = ['fullname', 'phone1', 'phone2', 'market_name', 'card_number', 'qr_image']


# ───────────────────────────── MIJOZ ─────────────────────────────

class MijozCreateSerializer(serializers.ModelSerializer):
    sotuvchilarim = serializers.PrimaryKeyRelatedField(
        queryset=Sotuvchi.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Mijoz
        fields = ['tg_id', 'fullname', 'phone1', 'phone2', 'sotuvchilarim']


class MijozListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mijoz
        fields = ['id', 'tg_id', 'fullname', 'phone1', 'created_at']


class MijozDetailSerializer(serializers.ModelSerializer):
    sotuvchilarim = SotuvchiListSerializer(many=True, read_only=True)

    class Meta:
        model = Mijoz
        fields = '__all__'


class MijozUpdateSerializer(serializers.ModelSerializer):
    sotuvchilarim = serializers.PrimaryKeyRelatedField(
        queryset=Sotuvchi.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Mijoz
        fields = ['fullname', 'phone1', 'phone2', 'sotuvchilarim']


# ───────────────────────────── QARZLAR ─────────────────────────────

class QarzlarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qarzlar
        fields = [
            'sotuvchi', 'mijoz', 'pul_miqdori',
            'qarz_sorov_tg_id', 'image',
        ]

    def validate(self, attrs):
        sotuvchi = attrs.get('sotuvchi')
        mijoz = attrs.get('mijoz')
        if not mijoz.sotuvchilarim.filter(pk=sotuvchi.pk).exists():
            raise serializers.ValidationError(
                "Bu mijoz ushbu sotuvchiga bog'liq emas."
            )
        return attrs


class QarzlarListSerializer(serializers.ModelSerializer):
    sotuvchi_nomi = serializers.CharField(source='sotuvchi.fullname', read_only=True)
    mijoz_nomi = serializers.CharField(source='mijoz.fullname', read_only=True)

    class Meta:
        model = Qarzlar
        fields = [
            'id', 'sotuvchi_nomi', 'mijoz_nomi',
            'pul_miqdori', 'status', 'qarz_created_at',
        ]


class QarzlarDetailSerializer(serializers.ModelSerializer):
    sotuvchi = SotuvchiListSerializer(read_only=True)
    mijoz = MijozListSerializer(read_only=True)

    class Meta:
        model = Qarzlar
        fields = '__all__'


class QarzlarStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qarzlar
        fields = ['status', 'qarz_tasdiq_tg_id']

    def validate(self, attrs):
        status = attrs.get('status')
        tasdiq_tg_id = attrs.get('qarz_tasdiq_tg_id')
        if status == Qarzlar.Status.TASDIQLANGAN and not tasdiq_tg_id:
            raise serializers.ValidationError(
                "Tasdiqlash uchun qarz_tasdiq_tg_id kiritilishi shart."
            )
        return attrs


# ───────────────────────────── TOLOVLAR ─────────────────────────────

class TolovlarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tolovlar
        fields = ['sotuvchi', 'mijoz', 'pul_miqdori', 'sotuvchi_tg_id']

    def validate(self, attrs):
        sotuvchi = attrs.get('sotuvchi')
        mijoz = attrs.get('mijoz')
        if not mijoz.sotuvchilarim.filter(pk=sotuvchi.pk).exists():
            raise serializers.ValidationError(
                "Bu mijoz ushbu sotuvchiga bog'liq emas."
            )
        return attrs


class TolovlarListSerializer(serializers.ModelSerializer):
    sotuvchi_nomi = serializers.CharField(source='sotuvchi.fullname', read_only=True)
    mijoz_nomi = serializers.CharField(source='mijoz.fullname', read_only=True)

    class Meta:
        model = Tolovlar
        fields = [
            'id', 'sotuvchi_nomi', 'mijoz_nomi',
            'pul_miqdori', 'created_at', 'tasdiq_time',
        ]


class TolovlarDetailSerializer(serializers.ModelSerializer):
    sotuvchi = SotuvchiListSerializer(read_only=True)
    mijoz = MijozListSerializer(read_only=True)

    class Meta:
        model = Tolovlar
        fields = '__all__'


class TolovlarTasdiqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tolovlar
        fields = ['tasdiq_time']

    def validate_tasdiq_time(self, value):
        from django.utils import timezone
        if value and value > timezone.now():
            raise serializers.ValidationError("Tasdiqlash vaqti kelajakda bo'lishi mumkin emas.")
        return value
    