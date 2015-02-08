#include<iostream>
#include<list>

using namespace std;

class graph
{
	int v;
	list<int> *adj;

public:
	graph(int v);
	void addEdge(int v, int w);
	bool isReachable(int s, int d);
};

graph::graph(int v)
{
	this->v = v;
	adj = new list<int> [v]; 
}

void graph::addEdge(int v, int w);
{
	adj[v].push_back(w);
}

bool isReachable(int s, int d)
{
	if (s==d)
		return true;
	bool *visited = new bool[v];

	for(int i = 0; i<v; i++)
	{
		visited[i] = false;
	}

	list<int> queue;

	visited[s] = true;
	queue.push_back(s);

	list<int>::iterator i;

	while (!queue.empty())
	{
		s  = queue.front();
		queue.pop_front();

		for(i = adj[s].begin(); i!=adj[s].end(); ++i)
		{
			if(*i==d)
				return true;
			if(!visited[*i])
			{
				visited[*i] =true;
				queue.push_back(*i);
			}
		} 
	}
	return false;
}

int main()
{
	graph g(4);
	g.addEdge(0, 1);
    g.addEdge(0, 2);
    g.addEdge(1, 2);
    g.addEdge(2, 0);
    g.addEdge(2, 3);
    g.addEdge(3, 3);
 
 	int u = 1, v = 3;
    if(g.isReachable(u, v))
        cout<< "\n There is a path from " << u << " to " << v;
    else
        cout<< "\n There is no path from " << u << " to " << v;
 
    u = 3, v = 1;
    if(g.isReachable(u, v))
        cout<< "\n There is a path from " << u << " to " << v;
    else
        cout<< "\n There is no path from " << u << " to " << v;
 
	return 0;
}