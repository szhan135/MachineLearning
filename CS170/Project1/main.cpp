//CS170 Project 1
//Author: Siyi Zhan
//SID: 862053955

#include <iostream>
#include <string>
#include <queue>

using namespace std;

class Node {
    public:
        int data[3][3];//num of puzzles
        int level;
        int fval;//for the f(n)=g(n)+h(n）
        Node(int data[3][3], int level, int fval);
};
Node::Node(int data[3][3], int level, int fval){
    this->data = data;
    this->level = level;
    this->fval = fval;
}
// class Puzzle {
//     private:
//         int size;
//         int open[10];
//         int closed[10];
//     public:
//         int Cal_Fval(Node start, Node goal);
//         int H_MisTile(Node start, Node goal);
// };
Node generate_child(int data[3][3], int level);
vector<int> Find(int data[3][3]);
void shuffle(int data[3][3], int x1, int y1, int x2, int y2);
int Cal_Fval(Node start, Node goal);
int H_MisTile(Node start, Node goal);
void process2(int data[3][3], int goal_data[3][3]);

Node generate_child(int data[3][3]){//the fuction returns the children from the root/parents
    int size;
    Node children[size];
    Node child = new Node(data,0,0);
    //find the blank, in my code is "0", get the pair of position
    vector<int> pairOfPos = Find(data); //now we have the position
    //show the up, down, left, right directions
    vector<int> up;
    vector<int> down;
    vector<int> left;
    vector<int> right;
    up.push_back(pairOfPos[0]);//up (x,y-1)
    up.push_back(pairOfPos[1]-1);
    down.push_back(pairOfPos[0]);//down (x,y+1)
    down.push_back(pairOfPos[1]+1);
    left.push_back(pairOfPos[0]-1);//left (x-1,y)
    left.push_back(pairOfPos[1]);
    right.push_back(pairOfPos[0]+1);//right (x+1,y)
    right.push_back(pairOfPos[1]);
    vector<int> directions[4] = {up, down, left, right}; 
    //Store all possible children in the array
    for (int i = 0; i<4; ++i){
        shuffle(data, pairOfPos[0], pairOfPos[1],directions[i][0],directions[i][1]);
        if(data.empty()==false){
        child = Node(data,child.level+1,0);
        children.append(child);
        }
    }
    return children;//generate all children in the array
}

vector<int> Find(dint data[3][3]){//Find the blank
    vector<int> pairOfPos;
    for (int i = 0; i<3; ++i){
        for (int j = 0; j<3;++j){
            if(data[i][j]==0){
                pairOfPos.push_back(i);
                pairOfPos.push_back(j);
            }
        }
    }
    return pairOfPos;
}

void shuffle(int data[3][3], int x1, int y1, int x2, int y2)//Display the move of the blank
{
    //data = this.data;
    int temp_puz[3][3];
    int temp[3][3];
    if(x2>=0 && x2<3 && y2>=0 && y2<=3){
        temp_puz = data;
        temp = temp_puz[x2][y2];
        temp_puz[x2][y2] = temp_puz[x1][y1];
        temp_puz[x1][y1] = temp;
        data = temp_puz;//now the data is after moving
    }
}

int Cal_Fval(Node start, Node goal){
    return H_MisTile(start,goal)+start.level;//return fval
}

int H_MisTile(Node start, Node goal){
    int temp = 0;
    for (int i=0;i<3;++i){
        for (int j=0;j<3;++j){
            if (start.data[i][j] != goal.data[i][j] && start.data[i][j] != 0){
                temp = temp+1;
            }
        }
    }
    return temp;//return h(n)
}

void process2(int start_puzzle[3][3], int goal_puzzle[3][3]){//process for MisTile when user enter 2
    int size;
    Node start = new Node(start_puzzle,0,0);
    Node goal = new Node(goal_puzzle,0,0);
    queue<Node> open;//open queue to store start nodes
    queue<Node> closed;//to store visited;
    start.fval = Cal_Fval(start,goal);
    open.append(start);
    Node cur = open.front();
    Node children[size] = generate_child(cur.data,cur.level);
    cout<<"The steps are as follows: "<<endl;
    if(H_MisTile(start,goal)!=0){
        for (int i = 0; i<3;++i){
            cout<<endl;
            for (int j = 0;j<=i;++j){
                cout<<cur.data[j]<<" ";
            }
        }
        cout<<endl<<endl;
        for (int i=0; i<size;++i){
            children[i].fval = Cal_Fval(children[i],goal);
            open.push(children[i]);
        }
        closed.push(cur);
        open.pop();
    }

}


int main() {
    // Node node= new Node;
    // Puzzle puzzle = new Puzzle;
    int userInteger = 0;
    int row_data[3];
    int num_puzzle[3][3];
    int goal_puzzle[3][3]={{1,2,3},{4,5,6},{7,8,0}};
    //vector<vector<int>, > 
    //start the game. Choose default puzzle or customlized puzzle
    cout<<"Welcome to 862053955 8 puzzle solver"<<endl;
    cout<<"Type '1' to use a default puzzle"<<endl;
    cout<<"Type '2' to enter your own puzzle"<<endl;
    //wait userInput
    cin >> userInteger;
    //if user choose to enter their own puzzle
    if (userInteger == 2){
        cout<<"Enter your puzzle, use a zero to represent the blank"<<endl;
        cout<<"Enter the first row, use space or tabs between numbers"<<endl;
        for(int i =0; i<=2;++i){
            cin>>userInteger;
            num_puzzle[0][i]=userInteger;
        }
        cout<<endl;
        cout<<"Enter the second row, use space or tabs between numbers"<<endl;
        for(int i =0; i<=2;++i){
            cin>>userInteger;
            num_puzzle[1][i]=userInteger;
        }
        cout<<endl;
        cout<<"Enter the third row, use space or tabs between numbers"<<endl;
        for(int i =0; i<=2;++i){
            cin>>userInteger;
            num_puzzle[2][i]=userInteger;
        }
        cout<<endl;

    }
    else{//the default puzzle data
        num_puzzle[3][3]={{1,0,3},{4,2,6},{7,5,8}};
    }
    //now we have the puzzle: from userInput or the default
    cout<<"Your start state is: "<<endl;
    for (int i=0; i<=2;++i){
        cout<<endl;
        for (int j=0; j<3; ++j){
            cout<<num_puzzle[i][j]<<" ";
        }
    }
    cout<<endl;
    //user Choose how to solve it
    cout<<"Enter your choice of algorithm:"<<endl;
    cout<<"1: Uniform Cost Search"<<endl;
    cout<<"2: A* with the Misplaced Tile heuristic"<<endl;
    cout<<"3: A* with the Eucledian distance heuristic"<<endl;
    //wait for userInput
    cin>>userInteger;
    if (userInteger == 1){
        //choose to solve with Uniform Cost Search
        //Call UniformSearch()

    }

    if (userInteger == 2){
        //choose to solve with A* with the Misplaced Tile heuristic
        //call MisTileHeuristic()
        process2(num_puzzle,goal_puzzle);
    }
    if(userInteger == 3){
        //choose to solve with A* with the Eucledian distance heuristic
        //call EuclDistHeursitic()
    }
    
    return 0;
}

