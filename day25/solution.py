t = open("input.txt","rt").read().split("\n\n")
f = lambda a,l:[ai+(c=="#") for ai,c in zip(a,l)]
g = lambda d:__import__('functools').reduce(f,d.splitlines(),[0]*d.find('\n'))
locks,keys = [g(d) for d in t if d[0]=="#"],[g(d) for d in t if d[0]!="#"]
print(sum(all(l+k<=7 for l,k in zip(ll,kk)) for ll in locks for kk in keys))