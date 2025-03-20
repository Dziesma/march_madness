import random
from collections import deque
import json


odds = json.load(open("odds.json"))
bracket = json.load(open("bracket.json"))

# American odds to implied probability
def odds_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        raise Exception("Encountered non-positive american odds")

# Simulate match
def simulate_match(team1, team2):
    prob1 = normalized_probabilities[team1]
    prob2 = normalized_probabilities[team2]
    total_prob = prob1 + prob2
    rand_value = random.uniform(0, total_prob)
    winner, winner_prob = (team1, prob1/total_prob) if rand_value < prob1 else (team2, prob2/total_prob)
    return winner, winner_prob

def walk_bracket(bracket):
    bracket_round = deque([match for reg in bracket.values() for match in reg])
    i = 1
    while bracket_round:
        print(f"Round {i}")
        print()
        bracket_round = walk_bracket_round(bracket_round)
        print()
        i+=1
        
def walk_bracket_round(this_round):
    next_round = deque()
    contender = None
    while this_round:
        team_A, team_B = this_round.popleft()
        winner, prob = simulate_match(team_A, team_B)
        print(f'{winner} beats {team_A if team_A != winner else team_B} with a {prob*100:.1f}% chance of winning')
        if not contender:
            contender = winner
        else:
            next_round.append((contender, winner))
            contender = None
    return next_round

# Probabilities for winning the championship
probabilities = {team: odds_to_probability(odds) for team, odds in odds.items()}

# Normalize probabilities
total_probability = sum(probabilities.values())
normalized_probabilities = {team: prob / total_probability for team, prob in probabilities.items()}


# Walk the bracket
walk_bracket(bracket)
