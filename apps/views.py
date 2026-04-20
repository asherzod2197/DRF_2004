from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Sotuvchi, Mijoz, Qarzlar, Tolovlar
from .serializers import (
    SotuvchiCreateSerializer, SotuvchiListSerializer,
    SotuvchiDetailSerializer, SotuvchiUpdateSerializer,

    MijozCreateSerializer, MijozListSerializer,
    MijozDetailSerializer, MijozUpdateSerializer,

    QarzlarCreateSerializer, QarzlarListSerializer,
    QarzlarDetailSerializer, QarzlarStatusUpdateSerializer,

    TolovlarCreateSerializer, TolovlarListSerializer,
    TolovlarDetailSerializer, TolovlarTasdiqSerializer,
)


class SotuvchiViewSet(viewsets.ModelViewSet):
    queryset = Sotuvchi.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return SotuvchiCreateSerializer
        if self.action in ('update', 'partial_update'):
            return SotuvchiUpdateSerializer
        if self.action == 'retrieve':
            return SotuvchiDetailSerializer
        return SotuvchiListSerializer

    def get_queryset(self):
        qs = Sotuvchi.objects.all()
        tg_id = self.request.query_params.get('tg_id')
        market_id = self.request.query_params.get('market_id')
        if tg_id:
            qs = qs.filter(tg_id=tg_id)
        if market_id:
            qs = qs.filter(market_id=market_id)
        return qs

    # GET /sotuvchilar/{id}/mijozlar/
    @action(detail=True, methods=['get'])
    def mijozlar(self, request, pk=None):
        sotuvchi = self.get_object()
        from .serializers import MijozListSerializer
        mijozlar = sotuvchi.mijozlar.all()
        serializer = MijozListSerializer(mijozlar, many=True)
        return Response(serializer.data)


class MijozViewSet(viewsets.ModelViewSet):
    queryset = Mijoz.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return MijozCreateSerializer
        if self.action in ('update', 'partial_update'):
            return MijozUpdateSerializer
        if self.action == 'retrieve':
            return MijozDetailSerializer
        return MijozListSerializer

    def get_queryset(self):
        qs = Mijoz.objects.all()
        tg_id = self.request.query_params.get('tg_id')
        phone = self.request.query_params.get('phone')
        if tg_id:
            qs = qs.filter(tg_id=tg_id)
        if phone:
            qs = qs.filter(phone1=phone)
        return qs

    # GET /mijozlar/{id}/sotuvchilar/
    @action(detail=True, methods=['get'])
    def sotuvchilar(self, request, pk=None):
        mijoz = self.get_object()
        serializer = SotuvchiListSerializer(mijoz.sotuvchilarim.all(), many=True)
        return Response(serializer.data)

    # POST /mijozlar/{id}/sotuvchi-qoshish/
    @action(detail=True, methods=['post'], url_path='sotuvchi-qoshish')
    def sotuvchi_qoshish(self, request, pk=None):
        mijoz = self.get_object()
        sotuvchi_id = request.data.get('sotuvchi_id')
        try:
            sotuvchi = Sotuvchi.objects.get(pk=sotuvchi_id)
        except Sotuvchi.DoesNotExist:
            return Response({'detail': 'Sotuvchi topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        mijoz.sotuvchilarim.add(sotuvchi)
        return Response({'detail': 'Sotuvchi muvaffaqiyatli qo\'shildi.'})

    # POST /mijozlar/{id}/sotuvchi-olib-tashlash/
    @action(detail=True, methods=['post'], url_path='sotuvchi-olib-tashlash')
    def sotuvchi_olib_tashlash(self, request, pk=None):
        mijoz = self.get_object()
        sotuvchi_id = request.data.get('sotuvchi_id')
        try:
            sotuvchi = Sotuvchi.objects.get(pk=sotuvchi_id)
        except Sotuvchi.DoesNotExist:
            return Response({'detail': 'Sotuvchi topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        mijoz.sotuvchilarim.remove(sotuvchi)
        return Response({'detail': 'Sotuvchi olib tashlandi.'})


class QarzlarViewSet(viewsets.ModelViewSet):
    queryset = Qarzlar.objects.select_related('sotuvchi', 'mijoz').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return QarzlarCreateSerializer
        if self.action == 'retrieve':
            return QarzlarDetailSerializer
        if self.action == 'status_update':
            return QarzlarStatusUpdateSerializer
        return QarzlarListSerializer

    def get_queryset(self):
        qs = Qarzlar.objects.select_related('sotuvchi', 'mijoz').all()
        sotuvchi_id = self.request.query_params.get('sotuvchi_id')
        mijoz_id = self.request.query_params.get('mijoz_id')
        status_filter = self.request.query_params.get('status')
        if sotuvchi_id:
            qs = qs.filter(sotuvchi_id=sotuvchi_id)
        if mijoz_id:
            qs = qs.filter(mijoz_id=mijoz_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    # PATCH /qarzlar/{id}/status-update/
    @action(detail=True, methods=['patch'], url_path='status-update')
    def status_update(self, request, pk=None):
        qarz = self.get_object()
        serializer = QarzlarStatusUpdateSerializer(qarz, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # GET /qarzlar/kutilmoqda/
    @action(detail=False, methods=['get'])
    def kutilmoqda(self, request):
        qs = self.get_queryset().filter(status=Qarzlar.Status.KUTILMOQDA)
        serializer = QarzlarListSerializer(qs, many=True)
        return Response(serializer.data)


class TolovlarViewSet(viewsets.ModelViewSet):
    queryset = Tolovlar.objects.select_related('sotuvchi', 'mijoz').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return TolovlarCreateSerializer
        if self.action == 'retrieve':
            return TolovlarDetailSerializer
        if self.action == 'tasdiqlash':
            return TolovlarTasdiqSerializer
        return TolovlarListSerializer

    def get_queryset(self):
        qs = Tolovlar.objects.select_related('sotuvchi', 'mijoz').all()
        sotuvchi_id = self.request.query_params.get('sotuvchi_id')
        mijoz_id = self.request.query_params.get('mijoz_id')
        if sotuvchi_id:
            qs = qs.filter(sotuvchi_id=sotuvchi_id)
        if mijoz_id:
            qs = qs.filter(mijoz_id=mijoz_id)
        return qs

    # PATCH /tolovlar/{id}/tasdiqlash/
    @action(detail=True, methods=['patch'])
    def tasdiqlash(self, request, pk=None):
        tolov = self.get_object()
        if tolov.tasdiq_time is not None:
            return Response(
                {'detail': 'Bu to\'lov allaqachon tasdiqlangan.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TolovlarTasdiqSerializer(tolov, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # GET /tolovlar/tasdiqlanmaganlar/
    @action(detail=False, methods=['get'])
    def tasdiqlanmaganlar(self, request):
        qs = self.get_queryset().filter(tasdiq_time__isnull=True)
        serializer = TolovlarListSerializer(qs, many=True)
        return Response(serializer.data)
    
    