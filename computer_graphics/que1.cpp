#include <GL/gl.h> 
#include <GL/glu.h> 
#include <GL/glut.h> // (or others, depending on the system in use)
#include <bits/stdc++.h>
using namespace std;

int a,b,c,d;

void init (void)
{
	glClearColor (1.0, 1.0, 1.0, 0.0); // Set display-window color to white.
	glMatrixMode (GL_PROJECTION); // Set projection parameters.
	gluOrtho2D (0, 500, 500, 1);// Orthogonal projection: [x,y,z]--->[x,y,0]
}

void plot_line_m_greater_1(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 < y2
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = a + 2 * b;
	int x = x1;
	int y = y1;
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
		glVertex2i(x,y);
	}
}

void plot_line_m_lesser_1(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 < y2 , so m is positive but less than 1
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = 2 * a + b;
	int x = x1;
	int y = y1;
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
		glVertex2i(x,y);
	}
}

void plot_line_mod_m_less_1_m_less_0(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 > y2 and mod m is less than 1
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = 2 * a - b;
	int x = x1;
	int y = y1;
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
		glVertex2i(x,y);
	}
}

void plot_line_mod_m_greater_1_less_0(int x1, int y1, int x2, int y2){
	// x1 < x2, y1 > y2 , so m is negative but greater than 1
	int del_y = y2 - y1;	
	int del_x = x2 - x1;
	int a = del_y;
	int b = -del_x;
	int c = y1 * del_x - x1 * del_y;
	int d = 2 * a - b;
	int x = x1;
	int y = y1;
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
		glVertex2i(x,y);
	}
}

void plot_line_m_0(int x1, int x2, int y){
	int x = x1;
	glVertex2i(x,y);
	while (x < x2) {
		x = x + 1;
		glVertex2i(x,y);
	}
}

void plot_line_m_inf(int x, int y1, int y2) {
	int y = y1;
	glVertex2i(x,y);
	while (y < y2) {
		y = y + 1;
		glVertex2i(x,y);
	}
}

void plot_line_m_1(int x1, int y1, int x2 ,int y2){
	int x = x1, y = y1;
	glVertex2i(x,y);
	while (x < x2) {
		x = x + 1;
		y = y + 1;
		glVertex2i(x,y);
	}
}

void plot_line_m_minus_1(int x1, int y1, int x2 ,int y2){
	int x = x1, y = y1;
	glVertex2i(x,y);
	while (x < x2) {
		x = x + 1;
		y = y - 1;
		glVertex2i(x,y);
	}
}

void plot_line(int x1, int y1, int x2 ,int y2) {
	if (x1 > x2) {
		int x = x1;
		x1 = x2;
		x2 = x;
		int y = y1;
		y1 = y2;
		y2 = y;
	}

	cout << x1 << " " << y1 << " " << x2 << " " << y2 << endl;

	float del_x = x2 - x1;
	float del_y = y2 - y1;
	float m;
	if (del_x == 0) {
		cout << "slope inf" << endl;
		if (y2 > y1)
			plot_line_m_inf(x1,y1,y2);
		else
			plot_line_m_inf(x1,y2,y1);
		return;
	} 
	m = del_y / del_x;

	if (m == 0) {
		cout << "slope is 0" << endl;
		if (x1 < x2)
			plot_line_m_0(x1,x2,y1);
		else
			plot_line_m_0(x2,x1,y1);
	}
	else if (m > 1) {
		cout << "M > 1" << endl;
		plot_line_m_greater_1(x1,y1,x2,y2);
	}
	else if (m > 0 && m < 1) {
		cout << "0 < M < 1" << endl;
		plot_line_m_lesser_1(x1,y1,x2,y2);
	}
	else if (m < 0 && abs(m) < 1) {
		cout << "M < 0, -M < 1" << endl;
		plot_line_mod_m_less_1_m_less_0(x1,y1,x2,y2);
	}
	else if (m < 0 && abs(m) > 1) {
		cout << "M < 0, -M > 1" << endl;
		plot_line_mod_m_greater_1_less_0(x1,y1,x2,y2);
	}
	else if (m == 1) {
		cout << "M = 1" << endl;
		plot_line_m_1(x1,y1,x2,y2);
	}
	else if (m == -1) {
		cout << "M = -1" << endl;
		plot_line_m_minus_1(x1,y1,x2,y2);
	}
}

void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT); // Clear display window.
	glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(1.0f); // Set point size
	glBegin(GL_POINTS);// Marks the beginning of the vertices list
		plot_line(a,b,c,d);
		//plot_line(0,150,180,0);
	glEnd( );
	glFlush( ); 
}
int main (int argc, char** argv)
{
	cin >> a >> b >> c >> d;
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
