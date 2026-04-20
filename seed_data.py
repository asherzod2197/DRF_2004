import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Django sozlamalari — loyiha nomingizga qarab o'zgartiring
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.utils import timezone
from apps.models import Sotuvchi, Mijoz, Qarzlar, Tolovlar 


def t(days_ago, hours=0):
    """Yordamchi: N kun oldingi timezone-aware datetime."""
    return timezone.now() - timedelta(days=days_ago, hours=hours)


def run():
    print("🧹 Eski ma'lumotlar tozalanmoqda...")
    Tolovlar.objects.all().delete()
    Qarzlar.objects.all().delete()
    Mijoz.objects.all().delete()
    Sotuvchi.objects.all().delete()

    # ─────────────────────────── SOTUVCHILAR ───────────────────────────
    print("👤 Sotuvchilar yaratilmoqda...")

    s1 = Sotuvchi.objects.create(
        tg_id=100000001,
        fullname="Jahongir Toshmatov",
        phone1="+998901234501",
        phone2="+998711234501",
        market_name="Jahon Savdo",
        card_number="8600123456781001",
        market_id=11001,
    )
    s2 = Sotuvchi.objects.create(
        tg_id=100000002,
        fullname="Sardor Yusupov",
        phone1="+998901234502",
        market_name="Sardor Market",
        card_number="8600123456781002",
        market_id=22002,
    )
    s3 = Sotuvchi.objects.create(
        tg_id=100000003,
        fullname="Nilufar Rahimova",
        phone1="+998901234503",
        phone2="+998931234503",
        market_name="Nilufar Do'koni",
        card_number="8600123456781003",
        market_id=33003,
    )

    sotuvchilar = [s1, s2, s3]
    print(f"   ✅ {len(sotuvchilar)} ta sotuvchi yaratildi.")

    # ─────────────────────────── MIJOZLAR ───────────────────────────
    print("🧑‍🤝‍🧑 Mijozlar yaratilmoqda...")

    m1 = Mijoz.objects.create(tg_id=200000001, fullname="Bobur Xasanov",    phone1="+998901110001")
    m2 = Mijoz.objects.create(tg_id=200000002, fullname="Dilnoza Karimova", phone1="+998901110002")
    m3 = Mijoz.objects.create(tg_id=200000003, fullname="Ulugbek Mirzayev", phone1="+998901110003")
    m4 = Mijoz.objects.create(tg_id=200000004, fullname="Shahnoza Sobirov", phone1="+998901110004")
    m5 = Mijoz.objects.create(tg_id=200000005, fullname="Firdavs Ergashev", phone1="+998901110005")
    m6 = Mijoz.objects.create(tg_id=200000006, fullname="Kamola Nazarova",  phone1="+998901110006")
    m7 = Mijoz.objects.create(tg_id=200000007, fullname="Sherzod Qodirov",  phone1="+998901110007")

    # Mijozlarni sotuvchilarga bog'lash
    m1.sotuvchilarim.add(s1, s2)        # Bobur — s1 va s2 da
    m2.sotuvchilarim.add(s1)            # Dilnoza — faqat s1 da
    m3.sotuvchilarim.add(s2, s3)        # Ulugbek — s2 va s3 da
    m4.sotuvchilarim.add(s1, s3)        # Shahnoza — s1 va s3 da
    m5.sotuvchilarim.add(s3)            # Firdavs — faqat s3 da
    m6.sotuvchilarim.add(s2)            # Kamola — faqat s2 da
    m7.sotuvchilarim.add(s1, s2, s3)    # Sherzod — hammada

    mijozlar = [m1, m2, m3, m4, m5, m6, m7]
    print(f"   ✅ {len(mijozlar)} ta mijoz yaratildi.")

    # ─────────────────────────── QARZLAR ───────────────────────────
    print("💸 Qarzlar yaratilmoqda...")

    qarzlar_data = [
        # (sotuvchi, mijoz, pul_miqdori, status, days_ago, sorov_tg_id, tasdiq_tg_id)
        (s1, m1, Decimal("500000"),   Qarzlar.Status.TASDIQLANGAN, 30,  m1.tg_id, s1.tg_id),
        (s1, m1, Decimal("250000"),   Qarzlar.Status.TASDIQLANGAN, 20,  m1.tg_id, s1.tg_id),
        (s1, m2, Decimal("750000"),   Qarzlar.Status.TASDIQLANGAN, 25,  m2.tg_id, s1.tg_id),
        (s1, m2, Decimal("1200000"),  Qarzlar.Status.KUTILMOQDA,   3,   m2.tg_id, None),
        (s1, m4, Decimal("300000"),   Qarzlar.Status.RAD_QILINGAN, 15,  m4.tg_id, s1.tg_id),
        (s1, m7, Decimal("2000000"),  Qarzlar.Status.TASDIQLANGAN, 10,  m7.tg_id, s1.tg_id),
        (s2, m1, Decimal("450000"),   Qarzlar.Status.TASDIQLANGAN, 22,  m1.tg_id, s2.tg_id),
        (s2, m3, Decimal("180000"),   Qarzlar.Status.KUTILMOQDA,   1,   m3.tg_id, None),
        (s2, m6, Decimal("900000"),   Qarzlar.Status.TASDIQLANGAN, 18,  m6.tg_id, s2.tg_id),
        (s2, m6, Decimal("600000"),   Qarzlar.Status.RAD_QILINGAN, 8,   m6.tg_id, s2.tg_id),
        (s2, m7, Decimal("1500000"),  Qarzlar.Status.KUTILMOQDA,   2,   m7.tg_id, None),
        (s3, m3, Decimal("350000"),   Qarzlar.Status.TASDIQLANGAN, 28,  m3.tg_id, s3.tg_id),
        (s3, m4, Decimal("2500000"),  Qarzlar.Status.TASDIQLANGAN, 14,  m4.tg_id, s3.tg_id),
        (s3, m5, Decimal("120000"),   Qarzlar.Status.KUTILMOQDA,   5,   m5.tg_id, None),
        (s3, m5, Decimal("800000"),   Qarzlar.Status.TASDIQLANGAN, 40,  m5.tg_id, s3.tg_id),
        (s3, m7, Decimal("1000000"),  Qarzlar.Status.RAD_QILINGAN, 12,  m7.tg_id, s3.tg_id),
        (s3, m4, Decimal("400000"),   Qarzlar.Status.KUTILMOQDA,   0,   m4.tg_id, None),
    ]

    qarz_objs = []
    for sotuvchi, mijoz, pul, stat, days, sorov_id, tasdiq_id in qarzlar_data:
        q = Qarzlar(
            sotuvchi=sotuvchi,
            mijoz=mijoz,
            pul_miqdori=pul,
            status=stat,
            qarz_sorov_tg_id=sorov_id,
            qarz_tasdiq_tg_id=tasdiq_id,
            qarz_created_at=t(days),
        )
        q.save()
        qarz_objs.append(q)

    print(f"   ✅ {len(qarz_objs)} ta qarz yaratildi.")

    # ─────────────────────────── TO'LOVLAR ───────────────────────────
    print("✅ To'lovlar yaratilmoqda...")

    tolovlar_data = [
        # (sotuvchi, mijoz, pul_miqdori, created_days_ago, tasdiq_days_ago | None)
        (s1, m1, Decimal("300000"),  28, 27),
        (s1, m2, Decimal("500000"),  23, 22),
        (s2, m1, Decimal("200000"),  20, 19),
        (s2, m6, Decimal("700000"),  16, 15),
        (s3, m3, Decimal("150000"),  26, 25),
    ]

    tolov_objs = []
    for sotuvchi, mijoz, pul, created_days, tasdiq_days in tolovlar_data:
        tolov = Tolovlar(
            sotuvchi=sotuvchi,
            mijoz=mijoz,
            pul_miqdori=pul,
            sotuvchi_tg_id=sotuvchi.tg_id,
            created_at=t(created_days),
            tasdiq_time=t(tasdiq_days) if tasdiq_days is not None else None,
        )
        tolov.save()
        tolov_objs.append(tolov)

    print(f"   ✅ {len(tolov_objs)} ta to'lov yaratildi.")

    # ─────────────────────────── XULOSA ───────────────────────────
    print("\n📊 Yaratilgan ma'lumotlar:")
    print(f"   Sotuvchilar : {Sotuvchi.objects.count()}")
    print(f"   Mijozlar    : {Mijoz.objects.count()}")
    print(f"   Qarzlar     : {Qarzlar.objects.count()}")
    print(f"     └ Tasdiqlangan : {Qarzlar.objects.filter(status=Qarzlar.Status.TASDIQLANGAN).count()}")
    print(f"     └ Kutilmoqda  : {Qarzlar.objects.filter(status=Qarzlar.Status.KUTILMOQDA).count()}")
    print(f"     └ Rad qilingan: {Qarzlar.objects.filter(status=Qarzlar.Status.RAD_QILINGAN).count()}")
    print(f"   To'lovlar   : {Tolovlar.objects.count()}")
    print("\n🎉 Seed muvaffaqiyatli yakunlandi!")


if __name__ == '__main__':
    run()