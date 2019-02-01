# from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import csv

class Introduction(Page):
    def is_displayed(self):
       return self.round_number == 1
    pass

class players(Page):
    def is_displayed(self):
       return self.round_number <= self.player.in_round(1).number
    def is_displayed(self):
       return self.round_number == 1
    form_model = models.Player
    form_fields = ['number']
    
class MyPage(Page):
    def is_displayed(self):
       return self.round_number <= self.player.in_round(1).number
    form_model = models.Player
    form_fields = ['name','pts']
    def vars_for_template(self):
        return {
            'id' : self.player.id_in_group,
	}

class ResultsWaitPage(WaitPage):
    def is_displayed(self):
       return self.round_number <= self.player.in_round(1).number
    def after_all_players_arrive(self):
       pass
       
class Results(Page):
    def is_displayed(self):
       return self.round_number <= self.player.in_round(1).number
    def vars_for_template(self):
        me = self.player
        rno=self.round_number
        agpts=0.0
        opp=me.other_player()
        opp2 =me.other_player2()
        pts_list=[0,0,0]
        pt=[]
        rank=0
        agpts_list=self.group.table_avg_data
        for i in range (3):
            if self.player.id_in_group == i+1:
                pts_list[i]=sum(list(x.pts for x in self.player.in_all_rounds()))
                agpts=agpts+self.player.in_round(rno).pts
            if opp.id_in_group ==i+1:
                pts_list[i]=sum(list(x.pts for x in opp.in_all_rounds()))
                agpts=agpts+opp.in_round(rno).pts
            if opp2.id_in_group ==i+1:
                pts_list[i]=sum(list(x.pts for x in opp2.in_all_rounds()))  
                agpts=agpts+opp2.in_round(rno).pts
        agpts=agpts/3
        if sum(p.pts for p in self.player.in_all_rounds()) == max(pts_list):
            rank=1
            return{
                'id' : self.player.id_in_group,
                'pts':sum(p.pts for p in self.player.in_all_rounds()),
                'aggpts':sum(float(x) for x in agpts_list()),
                'list2':agpts,
                'list':agpts_list(),
                'number':self.player.in_round(1).number,
            }
        elif sum(p.pts for p in self.player.in_all_rounds()) == min(pts_list):
            rank=3
            return{
                'id' : self.player.id_in_group,
                'pts':sum(p.pts for p in self.player.in_all_rounds()),
                'aggpts':sum(float(x) for x in agpts_list()),    
                'list2':agpts,
                'list':agpts_list(),
                'number':self.player.in_round(1).number,
            }
        else:
            rank=2
            return{
                'id' : self.player.id_in_group,
                'pts':sum(p.pts for p in self.player.in_all_rounds()),
                'aggpts':sum(float(x) for x in agpts_list()),
                'list2':agpts,
                'list':agpts_list(),
                'number':self.player.in_round(1).number,
            }
class Final(Page):
   def is_displayed(self):
       return self.round_number == self.player.in_round(1).number
   def vars_for_template(self):
        agpts_list=self.group.table_avg_data
        points = []
        points2 = []
        with open('mygame/points_data.csv' , 'r') as f:
            read_csv=csv.reader(f)
            for x in read_csv:
                z = sum([int(a) for a in x[1:]])
                points.append(z)
                y = [int(a) for a in x[1:]]
                points2.append(y)
        return {
            'range' : range(1, 4),
            'id' : self.player.id_in_group,
            'points2': points2,
	        'player_in_all_rounds': self.player.in_all_rounds(),
	        'pts': sum(p.pts for p in self.player.in_all_rounds()),
            'list':points,
	}
   pass


page_sequence = [
    Introduction,
    players,
    MyPage,
    ResultsWaitPage,
    Results,
    Final,]
