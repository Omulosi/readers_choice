import pandas as pd
from utils import get_matchup_entries, get_matchup_groups, get_matchups, get_winners


def scraper(session, headers=None):
    
    DATA = []
    
    print('Getting sections...\n')
    sections = get_matchup_groups(session)
    print('Getting categories...\n')
    categories = get_matchups(session)
    print("Getting winners...\n")
    winners = get_winners(session)
    
    
    print('Getting entries...\n')
    entries = []
    for section in sections:
        entry = get_matchup_entries(session, group_id=section.get("id"))
        entries.extend(entry)
    
    print(f"Total entries: {len(entries)}")
    
    
    for entry in entries:
        # category
        category = [c for c in categories if entry.get('matchup_id') == c.get('id')]
        category = category and category[0] or {}
        
        # section
        section = [s for s in sections if category.get('matchup_group_id') == s.get('id')]
        section = section and section[0] or {}
        
        # winner
        winner = [w for w in winners if w.get('matchup_entry_id') == entry.get('id')]
        winner = winner and winner[0] or {}
        
        print("\n----------------------------------------------")
        print(entry)
        print(category)
        print(section)
        print(winner)
        
        name, address = entry.get('name'), entry.get('address')
        category = category.get('name')
        section = section.get('name')
        rank = winner.get('rank')
        
        DATA.append((section, category, name, address, rank))
        DATA = sorted(DATA, key=lambda item: item[1])
        
    
    print(f"\nTotal items: {len(DATA)}")
        
    df  = pd.DataFrame(DATA, columns=['SECTION', 'CATEGORY', 'NAME', 'ADDRESS',  'RANK'])
    df.to_csv('readers_choice.csv')
    