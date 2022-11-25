#include <bits/stdc++.h>
using namespace std;

class tri_pts{
    float a, b, c, x, y;
    public:
        tri_pts(float a, float b, float c) {
            this->a = a;
            this->b = b;
            this->c = c;
        }
        void hto2d() {
            x = this->a/this->c;
            y = this->b/this->c;
        }      
        void get2d() {
            cout << x << " " << y << endl;
        }
};

vector<float> split_str(string s, char delimeter) {
    vector<float> v;
    string cur_value = "";
    for (int i = 0;i<s.length();i++) {
        if (s[i] == delimeter) {
            v.push_back(stof(cur_value));
            cur_value = "";
            continue;
        }
        cur_value += s[i];
    }
    v.push_back(stof(cur_value));
    return v;
}

void read_file(string filename) {
    string filedata;
    ifstream offfile(filename);
    int i = 0;
    while (getline(offfile, filedata)) {
        i++;
        if (i > 1 && i <= 10) {
            cout << "file_data : " << filedata << endl;
            vector<float> vv = split_str(filedata, ' ');
            for (int i = 0;i< vv.size() ;i++) {
                cout << vv[i] << " ";
            }
            cout << endl;
            continue;           
        }

        if (i >= 10) 
            break;
    }

    offfile.close();

}

int main() {
    read_file("images/cat01.off");
    return 0;
}

// class triangle {
//     public:
    
//     vector<float> v1, v2, v3, N , P;
//     triangle (vector<float> p1, vector<float> p2, vector<float> p3) {
//         v1.assign(p1.begin(), p1.end());           
//         v2.assign(p2.begin(), p2.end());           
//         v3.assign(p3.begin(), p3.end());    
//         normal();
//         plane();       
//     }

//     vector<float> diff(vector<float> p, vector<float> q) {
//         for (int i = 0;i< p.size() ;i ++) {
//             p[i] -= q[i];
//         }
//         return p;
//     }

//     vector<float> cross(vector<float> p, vector<float> q) {
//         vector<float> v;
//         v.resize(3);
//         v[0] = p[1] * q[2] - q[1] * p[2];
//         v[1] = - p[0] * q[2] + q[0] * p[2];
//         v[2] = p[0] * q[1] - q[0] * p[1];

//         return v;

//     }

//     float dot(vector<float> p, vector<float> q) {
//         float dot_val = 0.0f;
//         for (int i = 0;i< p.size();i++) {
//             dot_val += p[i] * q[i];
//         }
//         return dot_val;
//     }

//     void normal() {
//         N = cross(diff(v3, v2),diff(v1, v2));
//     }

//     void plane() {
//         P.assign(N.begin(), N.end());
//         P.push_back(-dot(N, v1));
//     }

// };

