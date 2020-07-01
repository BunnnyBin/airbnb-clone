import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models

#check-in과 check-out사이의 날짜 object 생성 - Reservation만으로는 사이에 날짜를 판단불가해서
class BookedDay(models.Model):
    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):  #for admin
        return str(self.day)

class Reservation(core_models.TimeStampedModel):

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey("users.User", related_name="reservations", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", related_name="reservations", on_delete=models.CASCADE)

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:  # new reservation
            start = self.check_in
            end = self.check_out
            differ = end - start
            existing_booked_day = BookedDay.objects.filter(day__range=(start, end), reservation__room=self.room).exists()  # __range
            if not existing_booked_day:
                super().save(*args, **kwargs) #왜냐하면 BookedDay는 Reservation를 ForeignKey로 가지므로
                for i in range(differ.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
            return
        return super().save(*args, **kwargs)

    def __str__(self):  #for admin
        return str(self.room)