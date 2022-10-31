import peasy.*;

PeasyCam cam;
Triangle triangles[];
Triangle spheres[];


float normalizeColor(float c)
{
  return map(c, -1, 1, 0, 255);  
}

int rows = 20;
int columns = 20;
float depth = 100;


class Triangle
{
  PVector p1, p2, p3;
  Triangle(PVector p1_, PVector p2_, PVector p3_)
  {
     p1 = p1_; 
     p2 = p2_; 
     p3 = p3_; 
  }
  
  PVector normal()
  {
    PVector line1 = PVector.sub(p2, p1);
    PVector line2 = PVector.sub(p3, p1);
    return (line1).cross(line2).normalize();
  }
  
  void show()
  {
    fill(getColor());
    beginShape();
    vertex(p1.x, p1.y, p1.z);
    vertex(p2.x, p2.y, p2.z);
    vertex(p3.x, p3.y, p3.z);
    endShape(CLOSE);
  }
  
  color getColor()
  {
    float camera_points[] = cam.getPosition();
    PVector camera_position = new PVector(camera_points[0], camera_points[1], camera_points[2]);
    PVector n = normal();
    PVector colors = n.cross(camera_position).normalize();
    
    float hue = 282 + colors.x * 40;
    //float hue = 180 + colors.x * 90;
    float saturation = normalizeColor(0.5 + colors.y/2);
    float brightness = saturation + colors.z * (255 - saturation)/2;
    float alpha = 255;
    
    color c = color(hue, saturation, brightness, alpha);
    
    return c;
  }
}

void plane()
{
  triangles = new Triangle[2*(rows - 1)*(columns -1)];
  
  float w = 2*width/rows; 
  float l = 2*height/columns;
  int i = 0;
  
  for (int x = 0; x < rows - 1; x++)
  {
     for(int y = 0; y < columns - 1; y++)
     {  
         PVector p1 = new PVector(x*w, y*l, depth*noise(x*w, y*l));
         PVector p2 = new PVector((x+1)*w, y*l, depth*noise((x+1)*w, y*l));
         PVector p3 = new PVector(x*w, (y+1)*l, depth*noise(x*w, (y+1)*l));
         PVector p4 = new PVector((x+1)*w, (y+1)*l, depth*noise((x+1)*w, (y+1)*l));        
         
         triangles[i++] = new Triangle(p2, p3, p1);
         triangles[i++] = new Triangle(p2, p4, p3);
         
     }
  }  
}

void disco_sphere()
{
  float radius = 500;
  int divisions = 40;
  float lon_divisions = TWO_PI/divisions;
  float lat_divisions = PI/divisions;
  
  spheres = new Triangle[divisions * divisions * 2];
  
  int i = 0;
  for(float alpha = 0; alpha < TWO_PI; alpha += lon_divisions)
  {
    for (float beta = 0; beta < PI; beta += lat_divisions)
    {
        float x1 = radius * cos(alpha) * sin(beta);
        float y1 = radius * sin(alpha) * sin(beta);
        float z1 = radius * cos(beta) + 0 * radius * noise(x1, y1);
        
        float x2 = radius * cos(alpha + lon_divisions) * sin(beta);
        float y2 = radius * sin(alpha + lon_divisions) * sin(beta);
        
        float x3 = radius * cos(alpha) * sin(beta + lat_divisions);
        float y3 = radius * sin(alpha) * sin(beta + lat_divisions);
        float z3 = radius * cos(beta + lat_divisions) + 0 * radius * noise(x3, y3);;
        
        float x4 = radius * cos(alpha + lon_divisions) * sin(beta + lat_divisions);
        float y4 = radius * sin(alpha + lon_divisions) * sin(beta + lat_divisions);
        
        PVector p1 = new PVector(x1, y1, z1);
        PVector p2 = new PVector(x2, y2, z1);
        PVector p3 = new PVector(x3, y3, z3);
        PVector p4 = new PVector(x4, y4, z3);
        
        
        spheres[i++] = new Triangle(p1, p2, p3);
        spheres[i++] = new Triangle(p2, p4, p3);
    }
  }
}

void setup()
{
  size(1500, 1000, P3D);
  stroke(120);
  
  cam = new PeasyCam(this, 1000);
  colorMode(HSB, 360, 255, 255, 255);
  
  plane();

  disco_sphere();
  
}

void draw()
{
  background(255);
  for (Triangle t: triangles)
  {
    pushMatrix();
    translate(-width, -height, 0);
    t.show();
    popMatrix();
  }
  
  for (Triangle t: spheres)
  {
    pushMatrix();
    t.show();
    popMatrix();
  } 
}
