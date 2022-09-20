#include <GL/gl.h> 
#include <GL/glu.h> 
#include <GL/glut.h> // (or others, depending on the system in use)
void init (void)
{
	glClearColor (1.0, 1.0, 1.0, 0.0); // Set display-window color to white.
	glMatrixMode (GL_PROJECTION); // Set projection parameters.
	gluOrtho2D (0, 600, 600, 1);// Orthogonal projection: [x,y,z]--->[x,y,0]
}
void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT); // Clear display window.
	glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(2.0f); // Set point size
	glBegin(GL_TRIANGLES);// Marks the beginning of the vertices list
		glVertex2i(10,10);
		glVertex2i(100,100);
		glVertex2i(100,10);
	glEnd( );
	glFlush( ); 
}
int main (int argc, char** argv)
{
	glutInit (&argc, argv); // Initialize GLUT.
	glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB); // Set display mode.
	glutInitWindowPosition (5, 5); // Set top-left display-window position.
	glutInitWindowSize (600, 600); // Set display-window width and height.
	glutCreateWindow("CSL7450: Example 1"); // Create display window.
	init ( ); // Execute initialization procedure.
	glutDisplayFunc(dispPoint); // Send graphics to display window.
	glutMainLoop ( ); // Display everything and wait.
}
