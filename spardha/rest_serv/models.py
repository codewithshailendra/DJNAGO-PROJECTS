from django.db import models
from django.contrib.auth.models import User
import uuid
import json

def upload_to(instance, filename):
    return "player_profile_imgs/{}/{}".format(instance.PlayerID, filename)

class College(models.Model):
    CollegeID=models.AutoField(primary_key=True,editable=False)
    CollegeName=models.CharField(max_length=40,unique=True,editable=False)
    def Create(name_field):
        if(College.objects.filter(CollegeName=name_field).exists()):
            return None
        college = College.objects.create(CollegeName=name_field)
        college.save()
        return college

class Player(models.Model):
    UserRef = models.OneToOneField(User, primary_key=False)
    PlayerID=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PlayerName=models.CharField(max_length=40)
    PlayerImage=models.ImageField(blank=True,null=True,upload_to=upload_to)
    CollegeRef=models.ForeignKey(College,on_delete=models.CASCADE,blank=True,null=True)
    Email=models.EmailField()
    PhoneNumber=models.CharField(max_length=15,blank=True,null=True)
    def Notify(self, Message, Priority=1):
        notification = UserNotification(NotificationText=Message, Priority=Priority, UserToNotify=self)
        notification.save()
        return
    def GetNotifications(self):
        notifications = UserNotification.objects.filter(UserToNotify=self)
        return notifications
    def Register(name_field, image_field, college_name, email_field, password_field, mob_field):
        if(User.objects.filter(username=email_field).exists()):
            return None
        elif(len(College.objects.filter(CollegeName=college_name))!=1):
            return None
        user_field = User.objects.create_user(username=email_field, password=password_field)
        user_field.save()
        player = Player.objects.create(UserRef=user_field, PlayerName=name_field, PlayerImage=image_field, Email=email_field,
                                        CollegeRef=College.objects.get(CollegeName=college_name), PhoneNumber=mob_field)
        player.save()
        return player

class Event(models.Model):
    EventID=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    EventName=models.CharField(max_length=25)
    Venue=models.TextField(max_length=300,blank=True,null=True)
    EventDateTime=models.DateTimeField(blank=True,null=True)
    MinPlayersReq=models.IntegerField(default=0)
    MaxPlayersReq=models.IntegerField(default=0)
    def NotifyTeams(self, Message, Priority=1):
        for team in self.RegisteredTeams.all():
            team.NotifyTeam(Message, Priority)
        
class Team(models.Model):
    TeamRef=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CoachName=models.CharField(max_length=40,blank=True,null=True)
    CollegeRef=models.ForeignKey(College,on_delete=models.CASCADE,blank=True,null=True)
    Leader=models.ForeignKey(Player, on_delete=models.CASCADE,blank=True,null=True,related_name="team_leader")
    Members=models.ManyToManyField(Player,related_name="team_members")
    EventRef=models.ForeignKey(Event,on_delete=models.CASCADE)
    def NotifyTeam(self, Message, Priority=1):
        for player in self.Members.all():
            player.Notify(Message, Priority)
    
class PersistentNotification(models.Model):
    NotificationID=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    NotificationText=models.CharField(max_length=200)
    Priority=models.IntegerField(default=1,blank=True)
    
class UserNotification(models.Model):
    NotificationID=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    NotificationText=models.CharField(max_length=200)
    Priority=models.IntegerField(default=1,blank=True)
    UserToNotify=models.ForeignKey(Player,on_delete=models.CASCADE)
    
