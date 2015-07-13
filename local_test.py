import pymangal as pm

m = pm.mangal(url='http://localhost:8000', suffix='/api/v1/', usr='test', key='9d00823baa5be60d788d079143d9785a4ffd3eec')
m2 = pm.mangal(url='http://localhost:8000', suffix='/api/v1/', usr='test2', key='300b54877dca81e4b2f1aa8a112c288ccc97f919')

# Test taxa
def create_taxa(api, data):
    filt = 'name__exact=' + data['name']
    matches = api.List('taxa', filters=filt)
    if matches['meta']['total_count'] == 0:
        data = m.Post('taxa', data)
    else:
        data = matches['objects'][0]
    return data

leleg = create_taxa(m, {'name': 'Lamellodiscus elegans', 'status': 'confirmed'})
ligno = create_taxa(m2, {'name': 'Lamellodiscus ignoratus', 'status': 'confirmed'})

leleg['description'] = "Lamellodiscus elegans, a species of the Lamellodiscus genus."
leleg = m.Patch('taxa', leleg)
print leleg['description']

leleg['description'] = "Awesome! Possum!"
leleg = m2.Patch('taxa', leleg)
print leleg['description']
