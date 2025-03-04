def each_section(train, test, which_sect):
    '''
        Cols prerequisite: ['section 1']
    '''

    # do checking of cols here

    mean_section_price = train.groupby(f'section {which_sect}')['price'].mean().sort_values()
    test['price'] = test[f'section {which_sect}'].map(mean_section_price)
    return test

