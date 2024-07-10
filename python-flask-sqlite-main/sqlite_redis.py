import redis

# conexão com o redis
r = redis.Redis(host="redis-12897.c12.us-east-1-4.ec2.redns.redis-cloud.com",
                port=12897,
                db=0,
                password='9bXWnQjto13hsEmheB1cgCQucIEH8NLS')




chave = "2"
rb = r.get(chave)
if not rb:
   cursor = conn.cursor()
   cursor.execute("select procodigo, prodesc, provalor::varchar from produto where procodigo = "+chave)
   records = cursor.fetchall()
   insertObject = []
   columnNames = [column[0] for column in cursor.description]
   for record in records:
       insertObject.append( dict( zip( columnNames , record ) ) )
   json_string = json.dumps(insertObject)
   #aqui entra o redis
   r.set(chave, json_string)
   #aqui vai expirar o cache em 25 segundos
   r.expire(chave,25)
   print('cacheando os dados do potgresql no redis!')
   print(json_string)
else:
    rutf8 = rb.decode("utf-8")
    json_str = json.loads(rutf8)
    print('pegando do redis os dados cacheados!')
    print(json_str)
    #print(json_str[0]['prodesc'])

conn.close()
r.close()