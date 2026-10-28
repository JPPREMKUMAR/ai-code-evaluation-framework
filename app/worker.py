"""Private worker for repository-owned, allowlisted solutions only."""
import json,sys

def validate(intervals):
    if not isinstance(intervals,list): raise ValueError("InvalidInterval")
    for pair in intervals:
        if (not isinstance(pair,list) or len(pair)!=2 or
            not all(isinstance(x,(int,float)) and not isinstance(x,bool) for x in pair) or pair[0]>pair[1]):
            raise ValueError("InvalidInterval")

def reference(intervals):
    validate(intervals);ordered=sorted(intervals,key=lambda p:(p[0],p[1]));out=[]
    for start,end in ordered:
        if out and start<=out[-1][1]:out[-1][1]=max(out[-1][1],end)
        else:out.append([start,end])
    return out

def misses_touching(intervals):
    validate(intervals);ordered=sorted(intervals,key=lambda p:(p[0],p[1]));out=[]
    for start,end in ordered:
        if out and start<out[-1][1]:out[-1][1]=max(out[-1][1],end)
        else:out.append([start,end])
    return out

def crashes_empty(intervals):
    validate(intervals);ordered=sorted(intervals,key=lambda p:(p[0],p[1]));first=ordered[0];out=[first]
    for start,end in ordered[1:]:
        if start<=out[-1][1]:out[-1][1]=max(out[-1][1],end)
        else:out.append([start,end])
    return out

SOLUTIONS={"reference":reference,"misses-touching":misses_touching,"crashes-empty":crashes_empty}

def main():
    problem_id,candidate_id=sys.argv[1:3]
    if problem_id!="merge-intervals" or candidate_id not in SOLUTIONS:
        print(json.dumps({"error":"UnknownAllowlistedSolution"}));return
    try: print(json.dumps({"output":SOLUTIONS[candidate_id](json.loads(sys.stdin.read()))}))
    except ValueError as exc: print(json.dumps({"error_type":str(exc)}))

if __name__=="__main__":main()
