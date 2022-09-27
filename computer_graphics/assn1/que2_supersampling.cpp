#include <GL/gl.h> 
#include <GL/glu.h> 
#include <GL/glut.h> // (or others, depending on the system in use)
#include <bits/stdc++.h>
using namespace std;


void init (void)
{
	glClearColor (1.0, 1.0, 1.0, 0.0); // Set display-window color to white.
	glMatrixMode (GL_PROJECTION); // Set projection parameters.
	gluOrtho2D (0, 500, 500, 1);// Orthogonal projection: [x,y,z]--->[x,y,0]
}

vector<pair<int,int>> plot_line_m_greater_1(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 < y2
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = a + 2 * b;
	int x = x1;
	int y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	while (x < x2) {
		if (d >= 0) {
			d = d + 2 * b;
			y = y + 1;
		}
		else {
			d = d + 2 * (a + b);
			x = x + 1;
			y = y + 1;
		}
		v.push_back({x,y});
	}
	return v;
}

vector<pair<int,int>> plot_line_m_lesser_1(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 < y2 , so m is positive but less than 1
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = 2 * a + b;
	int x = x1;
	int y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	while (x < x2) {
		if (d >= 0) {
			d = d + 2 * (a + b);
			y = y + 1;
			x = x + 1;
		}
		else {
			d = d + 2 * a;
			x = x + 1;
		}
		v.push_back({x,y});
	}
	return v;
}

vector<pair<int,int>> plot_line_mod_m_less_1_m_less_0(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 > y2 and mod m is less than 1
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = 2 * a - b;
	int x = x1;
	int y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	while (x < x2) {
		if (d >= 0) {
			d = d + 2 * a;
			x = x + 1;
		}
		else {
			d = d + 2 * (a - b);
			x = x + 1;
			y = y - 1;
		}
		v.push_back({x,y});
	}
	return v;

}

vector<pair<int,int>> plot_line_mod_m_greater_1_less_0(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 > y2 , so m is negative but greater than 1
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = 2 * a - b;
	int x = x1;
	int y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	while (x < x2) {
		if (d >= 0) {
			d = d + 2 * (a - b);
			y = y - 1;
			x = x + 1;
		}
		else {
			d = d - 2 * b;
			y = y - 1;
		}
		//cout << x << " " << y << endl;
		v.push_back({x,y}); 
	}
	return v;
}

vector<pair<int,int>> plot_line_m_0(int x1, int x2, int y){
	int x = x1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	while (x < x2) {
		x = x + 1;
		v.push_back({x,y});
	}
	return v;
}

vector<pair<int,int>> plot_line_m_inf(int x, int y1, int y2) {
	int y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	while (y < y2) {
		y = y + 1;
		v.push_back({x,y});
	}
	return v;
}

vector<pair<int,int>> plot_line_m_1(int x1, int y1, int x2 ,int y2){
	int x = x1, y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});		
	while (x < x2) {
		x = x + 1;
		y = y + 1;
		v.push_back({x,y});
	}
	return v;
}

vector<pair<int,int>> plot_line_m_minus_1(int x1, int y1, int x2 ,int y2){
	int x = x1, y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});	
	while (x < x2) {
		x = x + 1;
		y = y - 1;
		v.push_back({x,y});
	}
	return v;
}

vector<pair<int,int>> plot_line(int x1, int y1, int x2 ,int y2) {
	vector<pair<int,int>> v;
	if (x1 > x2) {
		int x = x1;
		x1 = x2;
		x2 = x;
		int y = y1;
		y1 = y2;
		y2 = y;
	}


	float del_x = x2 - x1;
	float del_y = y2 - y1;
	float m;
	if (del_x == 0) {
		if (y2 > y1)
			v = plot_line_m_inf(x1,y1,y2);
		else
			v = plot_line_m_inf(x1,y2,y1);
		return v;
	} 
	m = del_y / del_x;

	if (m == 0) {
		if (x1 < x2)
			v = plot_line_m_0(x1,x2,y1);
		else
			v = plot_line_m_0(x2,x1,y1);
	}
	else if (m > 1) {
		v = plot_line_m_greater_1(x1,y1,x2,y2);
	}
	else if (m > 0 && m < 1) {
		v = plot_line_m_lesser_1(x1,y1,x2,y2);
	}
	else if (m < 0 && abs(m) < 1) {
		v = plot_line_mod_m_less_1_m_less_0(x1,y1,x2,y2);
	}
	else if (m < 0 && abs(m) > 1) {
		v = plot_line_mod_m_greater_1_less_0(x1,y1,x2,y2);
	}
	else if (m == 1) {
		v = plot_line_m_1(x1,y1,x2,y2);
	}
	else if (m == -1) {
		v = plot_line_m_minus_1(x1,y1,x2,y2);
	}
	return v;
}

void raster_triangle_one(pair<int,int> p1, pair<int,int> p2, pair<int,int> p3) {
        vector<pair<int,int>> v1 = plot_line(p1.first,p1.second,p2.first,p2.second);
        for (auto x:v1) {
                plot_line(x.first,x.second,p3.first,p3.second);
        }
}

void raster_triangle(pair<int,int> p1, pair<int,int> p2, pair<int,int> p3) {
        raster_triangle_one(p1,p2,p3);
        raster_triangle_one(p3,p1,p2);
        raster_triangle_one(p2,p3,p1);
}


vector<vector<float>> average_out(vector<vector<int>> vn, int m) {
	int n = vn.size();// m should be a multiple of n;
	vector<vector<float>> v;
	v.resize(n/2);
	for (int i = 0;i<v.size();i++) {
		v[i].resize(n/2);
	}
	int n_m = n / m;

	for (int i = 0;i<n;i+=m) {
		for (int j =0;j<n;j+=m) {
			// at i,j;
			float avg_value = 0;
			for (int k = i;k<i+m;k++){
				for (int l = j;l<j+m;l++) {
					avg_value += (float) vn[k][l];
				}
			}
			avg_value /= m * m;
			v[i/m][j/m] = avg_value;
		}
	}
	return v;
}

void supersampling(pair<int,int> p1, pair<int,int> p2, pair<int,int> p3, vector<vector<int>> &v) {
	vector<pair<int,int>> v1 = plot_line(p1.first,p1.second,p2.first,p2.second);
	for (auto x:v1) {
		v[x.first][x.second] = 1;
		vector<pair<int,int>> vn = plot_line(x.first,x.second,p3.first,p3.second);
		for (auto y:vn) {
			v[y.first][y.second] = 1;
		}
	}

}

void raster_triangle(vector<vector<float>> vv) {
	int n = vv.size();
	for (int i = 0;i< n;i++) {
		for (int j = 0;j<n;j++) {
		//	cout << vv[i][j] << " ";
			if (vv[i][j] != 0) {
				float c = 1 - vv[i][j];
				glColor3f(c*1.0,c*1.0,c*1.0);
				glVertex2i(i,j);
			}
		}
		//cout << endl;
	}
}


void supersampling_triangle(pair<int,int> p1, pair<int,int> p2, pair<int,int> p3) {
	int n = 1000;
	vector<vector<int>> v(n, vector<int>(n,0));
	supersampling(p1,p2,p3,v);
	supersampling(p3,p1,p2,v);
	supersampling(p2,p3,p1,v);

	vector<vector<float>> vv = average_out(v,2);
	raster_triangle(vv);

}

void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT); // Clear display window.
	glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(2.0f); // Set point size
	glBegin(GL_POINTS);// Marks the beginning of the vertices list
		supersampling_triangle({5*2,5*2},{400*2,300*2},{110*2,400*2});	
	glEnd( );
	glFlush( ); 
}
int main (int argc, char** argv)
{
	glutInit (&argc, argv); // Initialize GLUT.
	glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB); // Set display mode.
	glutInitWindowPosition (10, 30); // Set top-left display-window position.
	glutInitWindowSize (1000, 1000); // Set display-window width and height.
	glutCreateWindow("CSL7450: Example 1"); // Create display window.
	init ( ); // Execute initialization procedure.
	glutDisplayFunc(dispPoint); // Send graphics to display window.
	glutMainLoop ( ); // Display everything and wait.
	return 0;
}
