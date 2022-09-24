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

int give_sign(pair<int,int> p1, pair<int,int> p2, pair<int,int> p) {
	pair<int,int> v1,v2;
	v1.first = p2.second - p1.second;
	v1.second = p1.first - p2.first;
	v2.first = p.first - p1.first;
	v2.second = p.second - p1.second;

	return v1.first * v2.first + v1.second * v2.second;
}

void raster_triangle(pair<int,int> p1, pair<int,int> p2, pair<int,int> p3) {
	int min_x = min(min(p1.first, p2.first), p3.first);
	int min_y = min(min(p1.second, p2.second), p3.second);
	int max_x = max(max(p1.first, p2.first), p3.first);
	int max_y = max(max(p1.second, p2.second), p3.second);
	
	for (int x=min_x; x <= max_x; x++) {
		for (int y = min_y; y <= max_y; y++) {
			pair<int,int> p;
			p.first = x;
			p.second = y;
			int sign1 = give_sign(p1, p2, p);
			int sign2 = give_sign(p2,p3,p);
			int sign3 = give_sign(p3,p1,p);
			//cout << sign1 << " " << sign2 << " " << sign3 << endl;  
			if (((sign1 <= 0) && (sign2 <=0) && (sign3 <=0)) || ((sign1 >= 0) && (sign2 >=0) && (sign3 >=0))) {
				glVertex2i(x,y);
			}
		}
	}

}

void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT); // Clear display window.
	glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(1.0f); // Set point size
	glBegin(GL_POINTS);// Marks the beginning of the vertices list
		raster_triangle({5,5}, {300,400}, {110,300});
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
