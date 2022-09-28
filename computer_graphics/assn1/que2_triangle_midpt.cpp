#include <GL/gl.h> 
#include <GL/glu.h> 
#include <GL/glut.h> // (or others, depending on the system in use)
#include <bits/stdc++.h>
using namespace std;

pair<int,int> p1,p2,p3;

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
	glVertex2i(x, y);
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
		glVertex2i(x,y);
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
	glVertex2i(x, y);
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
		glVertex2i(x,y);
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
	glVertex2i(x, y);
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
		glVertex2i(x,y);
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
	glVertex2i(x, y);
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
		glVertex2i(x,y);
	}
	return v;
}

vector<pair<int,int>> plot_line_m_0(int x1, int x2, int y){
	int x = x1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	glVertex2i(x,y);
	while (x < x2) {
		x = x + 1;
		v.push_back({x,y});
		glVertex2i(x,y);
	}
	return v;
}

vector<pair<int,int>> plot_line_m_inf(int x, int y1, int y2) {
	int y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});
	glVertex2i(x,y);
	while (y < y2) {
		y = y + 1;
		v.push_back({x,y});
		glVertex2i(x,y);
	}
	return v;
}

vector<pair<int,int>> plot_line_m_1(int x1, int y1, int x2 ,int y2){
	int x = x1, y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});		
	glVertex2i(x,y);
	while (x < x2) {
		x = x + 1;
		y = y + 1;
		v.push_back({x,y});
		glVertex2i(x,y);
	}
	return v;
}

vector<pair<int,int>> plot_line_m_minus_1(int x1, int y1, int x2 ,int y2){
	int x = x1, y = y1;
	vector<pair<int,int>> v;
	v.push_back({x,y});	
	glVertex2i(x,y);
	while (x < x2) {
		x = x + 1;
		y = y - 1;
		v.push_back({x,y});
		glVertex2i(x,y);
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

void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT); // Clear display window.
	glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(1.0f); // Set point size
	glBegin(GL_POINTS);// Marks the beginning of the vertices list
		//raster_triangle({5,5},{400,300},{110,400});
		raster_triangle(p1,p2,p3);		
	glEnd( );
	glFlush( ); 
}
int main (int argc, char** argv)
{
	cin >> p1.first >> p1.second >> p2.first >> p2.second >> p3.first >> p3.second;
	glutInit (&argc, argv); // Initialize GLUT.
	glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB); // Set display mode.
	glutInitWindowPosition (10, 30); // Set top-left display-window position.
	glutInitWindowSize (500, 500); // Set display-window width and height.
	glutCreateWindow("CSL7450: Example 1"); // Create display window.
	init ( ); // Execute initialization procedure.
	glutDisplayFunc(dispPoint); // Send graphics to display window.
	glutMainLoop ( ); // Display everything and wait.
	return 0;
}
