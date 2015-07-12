import pymangal as pm

m = pm.mangal(url='http://localhost:8000', suffix='/api/v1/', usr='test', key='9d00823baa5be60d788d079143d9785a4ffd3eec')
m2 = pm.mangal(url='http://localhost:8000', suffix='/api/v1/', usr='test2', key='300b54877dca81e4b2f1aa8a112c288ccc97f919')

# Test taxa
leleg = {'name': 'Lamellodiscus elegans', 'status': 'confirmed'}
filt = "name__exact=" + leleg['name']
matches = m.List('taxa', filters=filt)
if matches['meta']['total_count'] == 0:
    leleg = m.Post('taxa', leleg)
else:
    leleg = matches['objects'][0]

leleg['id'] = int(leleg['id'])
leleg['description'] = "Lamellodiscus elegans, a species of the Lamellodiscus genus."

leleg = m.Patch('taxa', leleg)

leleg['id'] = int(leleg['id'])
leleg['description'] = "Awesome! Possum!"

leleg = m2.Patch('taxa', leleg)

print leleg
