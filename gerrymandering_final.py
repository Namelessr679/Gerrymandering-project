import matplotlib.pyplot as plt
import numpy as np

FILE_NAME = 'districts.txt'
MIN_NUM_DISTRICTS = 2
EFFICIENCY_GAP_LIMIT = 8


def main():
    file = open(FILE_NAME, 'r')

    state = input('Which state do you want to look up? ')
    state = state.title()

    dem_surplus_total = 0
    rep_surplus_total = 0
    total_votes = 0
    district_count = 0

    districts = []
    dem_votes_list = []
    rep_votes_list = []

    print()
    print('District   Democratic Votes   Republican Votes   Surplus Democrat   Surplus Republican')

    for line in file:
        district = line.split(',')

        if district[0] == state:
            for count in range(1, len(district), 3):

                district_num = district[count]
                democratic_votes = int(district[count + 1])
                republican_votes = int(district[count + 2])
                votes = democratic_votes + republican_votes
                total_votes += votes

                districts.append(district_num)
                dem_votes_list.append(democratic_votes)
                rep_votes_list.append(republican_votes)

                district_count += 1

                if democratic_votes < republican_votes:
                    surplus_dem = democratic_votes
                    surplus_rep = republican_votes - ((democratic_votes + republican_votes) // 2 + 1)
                elif republican_votes < democratic_votes:
                    surplus_rep = republican_votes
                    surplus_dem = democratic_votes - ((democratic_votes + republican_votes) // 2 + 1)
                else:
                    surplus_rep = 0
                    surplus_dem = 0

                dem_surplus_total += surplus_dem
                rep_surplus_total += surplus_rep

                print(f'{district_num:>4} {democratic_votes:>18,} {republican_votes:>18,} {surplus_dem:>18,} {surplus_rep:>18,}')

    print()
    print(f'Total surplus Democratic votes: {dem_surplus_total:,}')
    print(f'Total surplus Republican votes: {rep_surplus_total:,}')

    if district_count > MIN_NUM_DISTRICTS:
        if dem_surplus_total > rep_surplus_total:
            eff_gap = ((dem_surplus_total - rep_surplus_total) / total_votes) * 100
            party = 'Republicans'
        elif rep_surplus_total > dem_surplus_total:
            eff_gap = ((rep_surplus_total - dem_surplus_total) / total_votes) * 100
            party = 'Democrats'

        if eff_gap > EFFICIENCY_GAP_LIMIT:
            congress_seat = (eff_gap) / (100 / district_count)
            print(f'Gerrymandering in {state} favoring {party} worth {round(congress_seat, 2)} congressional seats')
        else:
            print(f'No evidence of gerrymandering in {state}.')
    else:
        print(f'Gerrymandering computation only valid when more than {MIN_NUM_DISTRICTS} districts.')

    file.close()

    indices = np.arange(len(districts))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.bar(indices, dem_votes_list, color='blue', edgecolor='black')
    ax1.set_xlabel('Districts')
    ax1.set_ylabel('Votes')
    ax1.set_title(f'Democratic Votes in {state}')
    ax1.set_xticks(indices)
    ax1.set_xticklabels(districts, rotation=45)

    ax2.bar(indices, rep_votes_list, color='red', edgecolor='black')
    ax2.set_xlabel('Districts')
    ax2.set_ylabel('Votes')
    ax2.set_title(f'Republican Votes in {state}')
    ax2.set_xticks(indices)
    ax2.set_xticklabels(districts, rotation=45)

    plt.tight_layout()
    plt.show()


main()
