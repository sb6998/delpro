from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv

author = 'Saurabh Bhatia'

doc = """
Decision making using game theory
"""

class Constants(BaseConstants):
    name_in_url = 'mygame'
    players_per_group = 3
    num_rounds = 50
    stakes =c(100)
    instructions_template = 'mygame/Instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pts = models.FloatField()
    average=models.FloatField()
    name = models.StringField()
    number = models.PositiveIntegerField(min = 1 , max =50)
    def set_payoffs(self):
        players = self.get_players()
        name1 = players[0].name
        pts = [p.pts for p in players]
        average=(1/3)*sum(pts)  
        for p in players:
            rnum=p.round_number
            break
        if rnum == 1 #and data != '1':
            with open('mygame/mygame.csv','w') as f:
                writer_csv=csv.writer(f)
                writer_csv.writerow(str(rnum)+str(average))
        
        with open('mygame/mygame.csv','r') as f:
            reader=csv.reader(f)
            data = [r for r in reader]
            if data == []:
                data=[[0]]
            else:
                data=data[-1][0]
        for x in range(2,51):
            if rnum == x and data != str(x):
                with open('mygame/mygame.csv','a') as f:
                    writer_csv=csv.writer(f)
                    writer_csv.writerow(str(rnum)+str(average))
        else:
            pass

        with open('mygame/points_data.csv','r') as f:
            reader=csv.reader(f)
            data = [r for r in reader]
            
        if rnum ==1:
            with open('mygame/points_data.csv','w') as f:
                name2 = name1.split(",")
                z = name2 + pts
                writer_csv = csv.writer(f)
                writer_csv.writerow(z)
        else:
            for x in range(2,51):
                if rnum == x and rnum != len(data):
                    with open('mygame/points_data.csv','a') as f:
                        name2 = name1.split(",")
                        z = name2 + pts
                        writer_csv = csv.writer(f)
                        writer_csv.writerow(z)
        return ""
    def table_avg_data(self):
        with open('mygame/mygame.csv', 'r') as f:
            read_csv=csv.reader(f)
            l=[]
            for x in read_csv:
                x=x[1:]
                l.append("".join(x))
            used=[]
            for x in l:
                used.append(x)
            final=[]
            pla=self.get_players()
            for p in  pla:
                rno=p.round_number
                break
            counter=0
            for i in used:
                final.append(i)
                counter=counter+1
                if counter==rno:
                    break
        return(final)
    def other_player(self):
        return self.get_others_in_group()[0]   

class Player(BasePlayer):
    pts = models.PositiveIntegerField(min=0, max=100)
    rank=models.PositiveIntegerField()
    number = models.PositiveIntegerField(min = 1 , max =50)
    name = models.StringField()
    def other_player(self):
        pts = models.PositiveIntegerField(min=0, max=100)
        return self.get_others_in_group()[0]    
    def other_player2(self):
        pts = models.PositiveIntegerField(min=0, max=100)
        return self.get_others_in_group()[1]    
