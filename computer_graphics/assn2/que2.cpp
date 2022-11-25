#include <GL/gl.h> 
#include <GL/glu.h> 
#include <GL/glut.h> // (or others, depending on the system in use)
#include <bits/stdc++.h>
using namespace std;

void init (void)
{
    // glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glClearColor (1.0, 1.0, 1.0, 0.0); // Set display-window color to white.
	glMatrixMode (GL_PROJECTION); // Set projection parameters.
	gluOrtho2D (0, 500, 500, 1);// Orthogonal projection: [x,y,z]--->[x,y,0]

    glClearDepth(1.0f); // Set background depth to farthest
    glEnable(GL_DEPTH_TEST); // Enable depth testing for z-culling
    glDepthFunc(GL_LEQUAL); // Set the type of depth-test
    glShadeModel(GL_SMOOTH); // Enable smooth shading
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST); // Nice perspective corrections
}

void reshape(GLsizei width, GLsizei height) {
    GLfloat aspect = (GLfloat) width / (GLfloat) height;
    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0f, aspect, 0.0f, 1000.0f);
}

const bool ndc_c = true;

class tripts{
    public:
    vector<float> vf;
    pair<float,float> xy;
    tripts () {
        ;
    }
    tripts(float a, float b, float c) {
        vf.clear();
        vf.resize(3);
        vf[0] = a;
        vf[1] = b;
        vf[2] = c;
    }

    float dot(tripts t2) {
        float dot_val = 0.0f;
        for (int i = 0;i< 3;i++) {
            dot_val += vf[i] * t2.vf[i];
        }
        return dot_val;
    }

    tripts diff(tripts p) {
        vector<float> f;
        f.resize(3);
        for (int i = 0;i< p.vf.size() ;i ++) {
            f[i] = vf[i] - p.vf[i];
        }
        tripts dif(f[0], f[1], f[2]);
        return dif;
    }

    tripts cross(tripts q) {
        float l, m, n;
        l = vf[1] * q.vf[2] - q.vf[1] * vf[2];
        m = q.vf[0] * vf[2] - vf[0] * q.vf[2];
        n = vf[0] * q.vf[1] - q.vf[0] * vf[1];
        tripts cross_product(l,m,n);
        return cross_product;
    }

    void norm() {
        float mag = sqrt(vf[0] * vf[0] + vf[1] * vf[1] + vf[2] * vf[2]);
        vf[0] /= mag;
        vf[1] /= mag;
        vf[2] /= mag;
    }
};

tripts c_ndc(tripts val, float l, float r, float t, float b, float n, float f) {
    float xe = val.vf[0];
    float ye = val.vf[1];
    float ze = val.vf[2];
    float xnd = ((2 * n/(r - l)) * xe + ((r+l)/(r-l))*ze)/-ze;
    float ynd = ((2 * n/(t - b)) * ye + ((b+t)/(t-b))*ze)/-ze;
    float znd = (((n+f)/(n-f)) * ze + ((2*n*f)/(n-f)))/-ze;
    tripts tript(xnd, ynd, znd);
    return tript;
}

class triangle {
    public:
    
    tripts v1, v2, v3, N;
    vector<float> P;
    float intensity_c;
    triangle (tripts p1, tripts p2, tripts p3) {
        v1 = p1;
        v2 = p2;
        v3 = p3;   
        normal();
        plane();       
    }

    void shade(tripts l) {
        float ca=0.4f, cl=0.5f, cr=0.7f;
        int p = 4;
        tripts h = l;
        intensity_c = cr*ca + cr*cl*(max(0.0f,N.dot(l))+pow(N.dot(h),p));
    }

    void normal() {
        tripts vec1 = v2.diff(v1);
        tripts vec2 = v3.diff(v1); 
        N = vec1.cross(vec2);
    }

    void plane() {
        P.assign(N.vf.begin(), N.vf.end());
        P.push_back(-N.dot(v1));
    }

};

vector<tripts> pts;
vector<tripts> temp;
vector<triangle> faces;
vector<float> ndc_values(6);

void read_file(string filename) {
    char * stt= (char * )filename.c_str();
    freopen(stt, "r", stdin);
    // freopen("output.txt","w",stdout);
    string s; cin >> s;
    int np, nf, tp;
    cin >> np >> nf >> tp;
    float min_x = FLT_MAX;
    float max_x = FLT_MIN;
    float min_y = FLT_MAX;
    float max_y = FLT_MIN;
    float min_z = FLT_MAX;
    float max_z = FLT_MIN;
    for (int i = 0;i<np;i++) {
        float a,b,c;
        cin >> a >> b >> c;
        min_x = min(a,min_x);
        max_x = max(a,max_x);
        min_y = min(b,min_y);
        max_y = max(b,max_y);
        min_z = min(c,min_z);
        max_z = max(c,max_z);
        temp.push_back(tripts(a,b,c));
    }

    ndc_values[0] = min_x-5; // l
    ndc_values[1] = max_x+5; // r
    ndc_values[2] = min_y-5; // b
    ndc_values[3] = max_y+5; // t
    ndc_values[4] = min_z-5; // n
    ndc_values[5] = max_z+5; // f

    float l = min_x-5;
    float r = max_x+5;
    float b = min_y-5;
    float t = max_y+5;
    float n = min_z-5;
    float f = max_z+5;


    if (ndc_c) {
        cout << "using ndc" << endl;
        for (tripts tri: temp) {
            tripts ndc_coor = c_ndc(tri, l, r, t, b, n ,f);
            pts.push_back(ndc_coor);
            // cout << ndc_coor.vf[0] << " " << ndc_coor.vf[1] << " " << ndc_coor.vf[2] << "\n"; 
        }
    } else {
        cout << "using normal coordinates" << endl;
        pts.assign(temp.begin(), temp.end());
    }
    
    for (int i = 0;i<nf;i++) {
        int npts, c1, c2, c3;
        cin >> npts >> c1 >> c2 >> c3;
        faces.push_back(triangle(pts[c1],pts[c2],pts[c3]));
    }
    
}

void pipeline(string filename) {
    read_file(filename);
    tripts l(0.0,0.0,1.0);
    l.norm();
    const float W = 1.0f;
    const float H = 1.0f;
    tripts C(0.0f,0.0f,-1.0f);
    cout << pts.size() << endl;
    cout << faces.size() << endl;
    vector<triangle> vv;
    for (int i = 0;i<faces.size();i++) {
        if (ndc_c) {
            if (faces[i].N.dot(C) > 0) {
                faces[i].shade(l);
                vv.push_back(faces[i]);
            }
        } else {
            if (faces[i].N.vf[2] > 0) {
                faces[i].shade(l);
                vv.push_back(faces[i]);
            }
        }
    }

    for (auto fac: vv) {
        float x1, y1, z1, x2, y2, z2, x3, y3, z3;
        x1 = fac.v1.vf[0];
        x2 = fac.v2.vf[0];
        x3 = fac.v3.vf[0];
        y1 = fac.v1.vf[1];
        y2 = fac.v2.vf[1];
        y3 = fac.v3.vf[1];
        z1 = fac.v1.vf[2];
        z2 = fac.v2.vf[2];
        z3 = fac.v3.vf[2];
        if (ndc_c) {
            x1 *= W;
            x2 *= W;
            x3 *= W;
            y1 *= H;
            y2 *= H;
            y3 *= H;
        }

        glColor3f(1.0 * fac.intensity_c,0.0*fac.intensity_c,0.0 * fac.intensity_c);
        glVertex2f(x1,y1);
        glVertex2f(x2,y2);
        glVertex2f(x3,y3);
    }

}

string offfilename;


void dispPoint (void)
{
	glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Clear display window.
	glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glColor3f (1.0, 0.0, 0.0); // Set point color to green.
	glPointSize(1.0f); // Set point size
    glTranslatef(0.0f, 0.0f, -400.0f);
	glBegin(GL_TRIANGLES);// Marks the beginning of the vertices list
        pipeline(offfilename);
	glEnd( );
	// glFlush( ); 
    glutSwapBuffers();
}


int main (int argc, char** argv)
{
    cout << "enter file path to run: " << endl;
    cin >> offfilename;
	glutInit (&argc, argv); // Initialize GLUT.
	glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB); // Set display mode.
	glutInitWindowPosition (10, 30); // Set top-left display-window position.
	glutInitWindowSize (500, 500); // Set display-window width and height.
	glutCreateWindow("CSL7450: Example 1"); // Create display window.
	glutDisplayFunc(dispPoint); // Send graphics to display window.
	glutReshapeFunc(reshape);
    init ( ); // Execute initialization procedure.
	glutMainLoop ( ); // Display everything and wait.
	return 0;
}
