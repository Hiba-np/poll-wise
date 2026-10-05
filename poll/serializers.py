from rest_framework import serializers
from poll.models import CustomeUser,poll,choice,voting

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomeUser
        fields=["email","password","username","phone","id"]
        read_only_fields=["id"]
    def create(self, validated_data):
        return CustomeUser.objects.create_user(**validated_data)

class ChoiceSerializer(serializers.ModelSerializer):
    votes=serializers.SerializerMethodField()
    voters=serializers.SerializerMethodField()
    class Meta:
        model=choice
        fields="__all__"
        read_only_fields=["id","poll_object"]
    def get_votes(self,object):
        vote_qs=voting.objects.filter(choice_object=object)
         # serializer_instance=VotingSerializer(vote_qs,many=True)
        return vote_qs.count()
    def get_voters(self,object):
            vote_qs=voting.objects.filter(choice_object=object)
             # serializer_instance=VotingSerializer(vote_qs,many=True)
            return vote_qs.values_list('owner_object__username',flat=True)
    



class PollSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField(read_only=True)
    choices=serializers.SerializerMethodField()
    class Meta:
        model=poll
        fields="__all__"
        read_only_fields=["created_at","is_active"]
    def get_choices(self,object):
        choice_qs=choice.objects.filter(poll_object=object)
        serializer_instance=ChoiceSerializer(choice_qs,many=True)
        return serializer_instance.data
    def get_total_vote(self,object):
        vote_qs=voting.objects.filter(poll_object=object)
        # serializer_instanse=VotingSerializer(vote_qs,many=True)
        return vote_qs.count()

# class ChoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=choice
#         fields="__all__"
#         read_only_fields=["id","poll_object"]

class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model=voting
        fields="__all__"
        read_only_fields=['owner_object','poll_object','id']
    