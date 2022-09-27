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

void plot_line(int x1, int y1, int x2 ,int y2){
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
void draw_circle(int a, int b, int r){
	double angle = 35 * (3.14/180);
	int x = -r;
	int y = 0;
	int h = 5 - 4 * r;
	glVertex2i(x + a, y + b);
	while (x < -r * cos(angle)) {
		if (h <= 0) {
			h = h + 4 * (3 - 2 * y);
			y = y - 1;
		} else {
			h = h + 4 * (5 + 2 * (x - y));
			x = x + 1;
			y = y - 1;
		}
		glVertex2i(x+a,y+b);	
	}

	double angle1 = 45 * (3.14 / 180);
	int x1 = -r * cos(angle1);
	int y1 = r * sin(angle1);
	int d = 5 - 4 * (x1 + 2 * y1) + 4 * (x1 * x1 + y1 * y1 - r * r);
	//int d = 5/4 + (3/sqrt(2)) * r;
	glVertex2i(x1+a,y1+b);
	while (y1 > 0) {
		if (d <= 0) {
			d = d + 4 * (5 - 2 * (x1 + y1));
			x1--;
			y1--;
		} else {
			d = d + 4* (3 - 2 * y1);
			y1--;
		}
		glVertex2i(x1+a,y1+b);
	}
}

void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT); // Clear display window.
	glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(1.0f); // Set point size
	glBegin(GL_POINTS);// Marks the beginning of the vertices list
		glVertex2i(200,200);
		draw_circle(200,200,100);
		plot_line(0,0,200,200);
		plot_line_m_minus_1(0,400,200,200);
	glEnd( );
	glFlush( ); 
}
int main (int argc, char** argv)
{
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
