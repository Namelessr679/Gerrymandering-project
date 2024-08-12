"""
Name:Robel Solomon Gizaw
Date:10/25/2023
CSC 201
Project 2-Gerrymandering

This programs analyzes the voting in the state entered by the user for a particular election
whose data is stored in a file. The program displays that voting data from that state by district
in a stacked bar chart, displays the statistics by district used to determine gerrymandering,
and computes whether there was gerrymandering in this election in favor of the Democrats or Republicans.

Document Assistance: (who and what  OR  declare that you gave or received no assistance):
Received no assistance and gave no assistance

"""

from graphics2 import *

FILE_NAME = 'districts.txt'
MIN_NUM_DISTRICTS = 2
EFFICIENCY_GAP_LIMIT = 8

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 750
DEFAULT_BAR_HEIGHT = 20
SPACE_BETWEEN = 5


def main():

    file = open(FILE_NAME, 'r')

    #Fixes and capitalization errors with user input
    state = input('Which state do you want to look up? ')
    state = state.title()

    win = GraphWin(f"District overview for {state}", WINDOW_WIDTH, WINDOW_HEIGHT)

    dem_surplus_total = 0
    rep_surplus_total = 0
    total_votes = 0
    district_count = 0


    top_point = Point(WINDOW_WIDTH / 2, 0)
    bottom_point = Point(WINDOW_WIDTH / 2, WINDOW_HEIGHT)
    line = Line(top_point, bottom_point)
    line.setFill('black')
    line.draw(win)

    print()
    print('District   Democratic Votes   Republican Votes   Surplus Democrat   Surplus Republican')
    
    #loop through each line in file
    for line in file:
        district = line.split(',')

        #Checks if loop is at the district the user required
        if district[0] == state:
            district_amount = int(district[-3])
            if (SPACE_BETWEEN * district_amount) + (DEFAULT_BAR_HEIGHT * district_amount) > WINDOW_HEIGHT - SPACE_BETWEEN:
                new_length = ((WINDOW_HEIGHT - SPACE_BETWEEN) - (SPACE_BETWEEN * district_amount)) / district_amount
            else:
                new_length = DEFAULT_BAR_HEIGHT

            for count in range(1, len(district), 3):
                
                #Extracts necessary values
                district_num = district[count]
                democratic_votes = int(district[count + 1])
                republican_votes = int(district[count + 2])
                votes = democratic_votes + republican_votes
                total_votes += votes

                #checks when to draw a blank space for when there are no votes in a district

                if votes != 0:

                    bar_length = (democratic_votes / votes) * WINDOW_WIDTH

                    upper_right = Point(0, SPACE_BETWEEN * (district_count + 1) + new_length * (district_count))
                    lower_left = Point(WINDOW_WIDTH, (SPACE_BETWEEN + new_length) * (district_count + 1))
                    bar2 = Rectangle(upper_right, lower_left)
                    bar2.setFill('red')
                    bar2.draw(win)

                    upper_left = Point(0, SPACE_BETWEEN * (district_count + 1) + new_length * (district_count))
                    lower_right = Point(bar_length, (SPACE_BETWEEN + new_length) * (district_count + 1))
                    bar = Rectangle(upper_left, lower_right)
                    bar.setFill('blue')
                    bar.draw(win)


                district_count += 1

                #Calculates surplus votes
                if democratic_votes < republican_votes:
                    surplus_dem = democratic_votes
                    surplus_rep = republican_votes - ((democratic_votes + republican_votes) // 2 + 1)
                elif republican_votes < democratic_votes:
                    surplus_rep = republican_votes
                    surplus_dem = democratic_votes - ((democratic_votes + republican_votes) // 2 + 1)
                else:
                    surplus_rep = 0
                    surplus_dem = 0
                
                #Calculates total surplus vote
                dem_surplus_total = dem_surplus_total + surplus_dem
                rep_surplus_total = rep_surplus_total + surplus_rep
                

                #printing final answers
                print(f'{district_num:>4} {democratic_votes:>18,} {republican_votes:>18,} {surplus_dem:>18,} {surplus_rep:>18,}')


    print()
    print(f'Total surplus Democratic votes: {dem_surplus_total:,}')
    print(f'Total surplus Republican votes: {rep_surplus_total:,}')


    #Calculates if there has been any gerrymandering within the districts of the state inputed

    if district_count > MIN_NUM_DISTRICTS:
        if dem_surplus_total > rep_surplus_total:
            eff_gap = ((dem_surplus_total - rep_surplus_total) / total_votes) * 100
            party = 'Republicans'
        elif rep_surplus_total > dem_surplus_total:
            eff_gap = ((rep_surplus_total - dem_surplus_total) / total_votes) * 100
            party = 'Democrats'

        if eff_gap > EFFICIENCY_GAP_LIMIT:
            congress_seat = (eff_gap) / (100 / district_amount)
            print(f'Gerrymandering in {state} favoring {party} worth {round(congress_seat,2)} congressional seats')

        else:
            print(f'No evidence of gerrymandering in {state}.')
    else:    
            
        print(f'Gerrymandering computation only valid when more than {MIN_NUM_DISTRICTS} districts.')

    file.close()

    win.getMouse()
    win.close()

    
main()