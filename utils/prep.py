def split_sect(plate: str):
    prev_state,section_i='',0
    splits={}
    for p in plate+'?':
        # update current state
        current_state='digit' if p.isdigit() else 'str'

        # check for new section
        if prev_state!=current_state or p=='?':
            if section_i!=0:
                splits[section_i]=current_running_string
            section_i+=1
            current_running_string=p
        else:
            current_running_string+=p
        # push current back to prev state
        prev_state=current_state
    return splits[1], splits[2], splits[3], splits[4]