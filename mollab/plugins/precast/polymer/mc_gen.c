

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

/*
  This code generates a series of amorphous polymer chains on
  a FCC lattice 
    */ 

#define PI            3.14159265 
#define MAX_X         300
#define MAX_Y         300
#define MAX_Z         300
#define MAX_ATOMS     16000000
 

/* define data structures */

typedef struct atom_t ATOM;
struct atom_t{
  int chain;    /*chain number*/
  int nic;      /*number of atom in chain*/
  int x[3];      /*lattice occupied by the atom*/
  int spot;      /*spot or position of atom in lattice*/
  int type;      /*atom type*/
};

int site[MAX_X][MAX_Y][MAX_Z][4];  /*0 if site is unoccupied 1 if occupied*/
int loc_dens[MAX_X][MAX_Y][MAX_Z][4];  /*local density of site in terms of number of occupied nearest neighbor sites 0-12*/
int snd_dens[MAX_X][MAX_Y][MAX_Z][4];  /*2nd nearest neighbor density 0-6*/
int natom;       /*total number of atoms*/
float density;
int c_length;
int n_chains;
int seed;
int n_incs;
float lat;
float mass;
FILE *fp,*fq;
char *inf,*outf,fnames[1][40];
ATOM atom_list[MAX_ATOMS]; /*the array of atoms, the length will be Natom*/

static void read_input(void);
static void gen_pos(void);
static void write_file(void);

main()
{
  int i,j,k;

  inf = "mc_gen.input";
  outf = (char *)malloc(256);
  fp = fopen(inf,"r");
  if(fp==NULL) printf("input file not found\n");
  
  printf("enter read _input\n"); 
  read_input();
  printf("exit read _input\n"); 
  
  printf("exit read _input\n"); 
  srand(seed);
  printf("enter gen_pos\n");
  gen_pos();
  printf("enter write_file\n");
  fq = fopen(outf,"w");
  if(fq==NULL) printf("output file not found\n");
  write_file();
  printf("exit write_file\n");
  fclose(fq);
}

static void read_input(void)
{
  int i,j,k,m,u,v;
  int ii,jj,kk,mm;  
  char *keyw,buf[256];

/* Read output file name */ 

  fgets(fnames[0],sizeof(fnames[0]),fp);

/* Read approximate density */ 

  fgets(buf,sizeof(buf),fp);
  fgets(buf,sizeof(buf),fp);
  sscanf(buf,"%f",&density);

/* Read chain length*/ 

  fgets(buf,sizeof(buf),fp);
  fgets(buf,sizeof(buf),fp);
  sscanf(buf,"%d",&c_length);

/* Read number of chains*/ 

  fgets(buf,sizeof(buf),fp);
  fgets(buf,sizeof(buf),fp);
  sscanf(buf,"%d",&n_chains);

/* Read lattice size*/ 

  fgets(buf,sizeof(buf),fp);
  fgets(buf,sizeof(buf),fp);
  sscanf(buf,"%f",&lat);
  lat=lat/sqrt(2.0)*2.0;

/* Read random number seed*/ 

  fgets(buf,sizeof(buf),fp);
  fgets(buf,sizeof(buf),fp);
  sscanf(buf,"%d",&seed);

/* Read random number seed*/ 

  fgets(buf,sizeof(buf),fp);
  fgets(buf,sizeof(buf),fp);
  sscanf(buf,"%f",&mass);

  printf("den %f c_leng %d n_ch %d l_s %f seed %d \n",density,c_length,n_chains,lat,seed);

  fclose(fp);
  printf("create names \n");
  printf("fname is %s \n",fnames[0]);
  strncpy(outf,fnames[0],strlen(fnames[0])-1);
  printf("output file is is %s \n",outf);
}

static void gen_pos(void)
{  
  int i,j,k,m,u,v;
  int ii,jj,kk,mm,nn,n;
  int n_oc_sites,t_sites;
  int dx[3],dy[3],dz[3];
  int st_ld[12][4];
  int snd_ld[6][4];
  int snd_count,nn_count,total_dens,point;
  int prob_low,prob_high;
  int reset;
  double sqrt_2_2;
  double angle,va_mag,vb_mag,d_prod;
  double a[3],aa[3],va[3],vb[3],vc[3];
  double neigh[12][4],v_store[12][3],mag_store[12];
  char buf[256];
  
/* Determine the edge lengths in lattice units  from the density */
  sqrt_2_2=sqrt(2)/2.0;
  n_oc_sites=c_length*n_chains;
  t_sites=(int)(n_oc_sites/density);
  n_incs=(int)(cbrt(t_sites/4.0))+1.0;
  printf("%f %d %d %d \n",sqrt_2_2,n_oc_sites,t_sites,n_incs);
/* Initialize the sites as empty */

  natom=0; 
  for(i=0;i<n_incs;i++)
    { 
      for(j=0;j<n_incs;j++)
        { 
          for(k=0;k<n_incs;k++)
            { 
              for(m=0;m<4;m++)
                {
                  site[i][j][k][m]=0;
                  loc_dens[i][j][k][m]=0;
                  snd_dens[i][j][k][m]=0;
                }
            }
        }
    }

  for(u=0;u<n_chains;u++)
    {
      atom_list[natom].chain=u+1;
      atom_list[natom].nic=0;
      i=(int)n_incs*((double)rand()/(double)RAND_MAX);     
      j=(int)n_incs*((double)rand()/(double)RAND_MAX);     
      k=(int)n_incs*((double)rand()/(double)RAND_MAX);     
      m=(int)4*((double)rand()/(double)RAND_MAX);   
      if(site[i][j][k][m]==1)
        {
          u--;
        }
      else
        { 
          printf("n_incs %d i %d j %d k %d m %d\n",n_incs,i,j,k,m);
          atom_list[natom].x[0]=i;
          atom_list[natom].x[1]=j;
          atom_list[natom].x[2]=k;
          atom_list[natom].spot=m;
          atom_list[natom].type=1;
          site[i][j][k][m]=1; 
          natom++;
          for(v=1;v<c_length;v++)
            {
              printf("looking for neighbor %d \n",v);
              nn=0;
              nn_count=0;
              snd_count=0;
              angle=0;
              dx[1]=i;
              dy[1]=j;
              dz[1]=k;
              dx[2]=i+1;
              dy[2]=j+1;
              dz[2]=k+1;
              dx[0]=i-1;
              dy[0]=j-1;
              dz[0]=k-1;
              if(dx[2]==n_incs)
                {
                  dx[2]=0;
                }
              if(dy[2]==n_incs)
                {
                  dy[2]=0;
                }
              if(dz[2]==n_incs)
                {
                  dz[2]=0;
                }
              if(dx[0]<0)
                {
                  dx[0]=n_incs-1;
                }
              if(dy[0]<0)
                {
                  dy[0]=n_incs-1;
                }
              if(dz[0]<0)
                {
                  dz[0]=n_incs-1;
                }

              if(m==0)
                {
                  a[0]=0;
                  a[1]=0;
                  a[2]=0;
                }
              else if(m==1)
                { 
                  a[0]=0.5;
                  a[1]=0.5;
                  a[2]=0;
                }
              else if(m==2)
                { 
                  a[0]=0.5;
                  a[1]=0;
                  a[2]=0.5;
                }
              else
                { 
                  a[0]=0;
                  a[1]=0.5;
                  a[2]=0.5;
                }
              for(ii=0;ii<3;ii++)
                {
                  for(jj=0;jj<3;jj++)
                    {
                      for(kk=0;kk<3;kk++)
                        {
                          for(mm=0;mm<4;mm++)
                            {
                              if(mm==0)
                                {
                                  aa[0]=0;
                                  aa[1]=0;
                                  aa[2]=0;
                                }
                              else if(mm==1)
                                { 
                                  aa[0]=0.5;
                                  aa[1]=0.5;
                                  aa[2]=0;
                                }
                              else if(mm==2)
                                { 
                                  aa[0]=0.5;
                                  aa[1]=0;
                                  aa[2]=0.5;
                                }
                              else if(mm==3)
                                { 
                                  aa[0]=0;
                                  aa[1]=0.5;
                                  aa[2]=0.5;
                                }
                              aa[0]=aa[0]+ii-1;
                              aa[1]=aa[1]+jj-1;
                              aa[2]=aa[2]+kk-1;
                              va[0]=(double)aa[0]-(double)a[0];
                              va[1]=(double)aa[1]-(double)a[1];
                              va[2]=(double)aa[2]-(double)a[2];
                              va_mag=sqrt(va[0]*va[0]+va[1]*va[1]+va[2]*va[2]);
                              if(site[dx[ii]][dy[jj]][dz[kk]][mm]==0||(v==c_length-1&&site[dx[ii]][dy[jj]][dz[kk]][mm]==2))
                                {
                                  if(va_mag<=sqrt_2_2+.01)
                                    {
                                      loc_dens[dx[ii]][dy[jj]][dz[kk]][mm]++;
                                      st_ld[nn_count][0]=dx[ii];
                                      st_ld[nn_count][1]=dy[jj];
                                      st_ld[nn_count][2]=dz[kk];
                                      st_ld[nn_count][3]=mm;
                                      nn_count++;
                                    }
/*
                              else if(va_mag<=1.01)
                                {
                                  snd_dens[dx[ii]][dy[jj]][dz[kk]][mm]++;
                                  snd_ld[snd_count][0]=dx[ii];
                                  snd_ld[snd_count][1]=dy[jj];
                                  snd_ld[snd_count][2]=dz[kk];
                                  snd_ld[snd_count][3]=mm;
                                  snd_count++;
                                }
*/
                                  if(va_mag<sqrt_2_2)
                                    {
                                      printf("creating atoms too close to each other\n");
                                      exit(1);
                                    }
                                  if(va_mag<=sqrt_2_2+.01)
                                    {
                                      if(v!=1)
                                        {
                                          d_prod=va[0]*vb[0]+va[1]*vb[1]+va[2]*vb[2];
                                          angle=acos(d_prod/(va_mag*vb_mag))*180.0/PI;
                                        }
                                      if((angle<-60.0&&angle>-150.0)||(angle>60.0&&angle<150.0)||v==1)
                                        {
                                          neigh[nn][0]=dx[ii];
                                          neigh[nn][1]=dy[jj];
                                          neigh[nn][2]=dz[kk];
                                          neigh[nn][3]=mm;
                                          v_store[nn][0]=va[0];
                                          v_store[nn][1]=va[1];
                                          v_store[nn][2]=va[2];
                                          mag_store[nn]=va_mag;
                                          nn++;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
              if(nn==0)
                {
                  if(reset==1)
                    {
                      printf("has already been reset and still can not find a neighbor\n");
                      printf("chain %d atom %d \n",u,v);
                      exit(1);
                    } 
                  printf("there is not a free neighbor site and must reset\n");
                  reset=1;
                  site[i][j][k][m]=2;
                  natom--;
                  i=atom_list[natom].x[0];
                  j=atom_list[natom].x[1];
                  k=atom_list[natom].x[2];
                  m=atom_list[natom].spot;
                  for(ii=0;ii<12;ii++)
                    {
                      loc_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]--;
                    }
/*
                  for(ii=0;ii<6;ii++)
                    {
                      snd_dens[snd_ld[ii][0]][snd_ld[ii][1]][snd_ld[ii][2]][snd_ld[ii][3]]--;
                    }
*/
                  vb[0]=vc[0];
                  vb[1]=vc[1];
                  vb[2]=vc[2];
                  v=v-2;
                }
              else
                {
                  total_dens=0;
                  for(ii=0;ii<nn;ii++)
                    {
                      total_dens=total_dens+(12-loc_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]);
/*
                      total_dens=total_dens+(6-snd_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]);
*/
                    }
                  point=total_dens*((double)rand()/(double)RAND_MAX);
                  prob_low=0;
                  prob_high=(12-loc_dens[st_ld[0][0]][st_ld[0][1]][st_ld[0][2]][st_ld[0][3]]);
/*
                  prob_high=prob_high+(6-snd_dens[st_ld[0][0]][st_ld[0][1]][st_ld[0][2]][st_ld[0][3]]);
*/
                  printf("span %d prob_high %d prob_low %d point %d\n",prob_high-prob_low,prob_high,prob_low,point);
                  printf("0 %d 1 %d 2 %d 3 %d \n",st_ld[0][0],st_ld[0][1],st_ld[0][2],st_ld[0][3]);
                  printf("site %d\n",site[st_ld[0][0]][st_ld[0][1]][st_ld[0][2]][st_ld[0][3]]);
                  for(ii=0;ii<nn;ii++)
                    {
                      if(point>=prob_low&&point<prob_high)
                        {
                          i=neigh[ii][0];
                          j=neigh[ii][1];
                          k=neigh[ii][2];
                          m=neigh[ii][3];
                          atom_list[natom].x[0]=i;
                          atom_list[natom].x[1]=j;
                          atom_list[natom].x[2]=k;
                          atom_list[natom].spot=m;
                          atom_list[natom].type=1;
                          atom_list[natom].chain=u+1;
                          site[i][j][k][m]=1;
                          natom++;             

                      /*store the previous vector*/
                          vc[0]=vb[0];
                          vc[1]=vb[1];
                          vc[2]=vb[2];
                          vb[0]=-v_store[ii][0];
                          vb[1]=-v_store[ii][1];
                          vb[2]=-v_store[ii][2];
                          vb_mag=mag_store[ii];
                          ii=nn;
                          reset=0;
                        }
                      else
                        {
                          if(ii==nn-1)
                            {
                              if(reset==1)
                                {
                                   printf("there is not a free neighbor site and must reset\n");
                                   printf("has already been reset and still can not find a neighbor\n");
                                   printf("chain %d atom %d \n",u,v);
                                   exit(1);
                                 } 
                               printf("resetting\n");           
                               reset=1;
                               site[i][j][k][m]=2;
                               natom--;
                               i=atom_list[natom].x[0];
                               j=atom_list[natom].x[1];
                               k=atom_list[natom].x[2];
                               m=atom_list[natom].spot;
                               for(ii=0;ii<12;ii++)
                                 {
                                   loc_dens[st_ld[ii][0]][st_ld[ii][1]][st_ld[ii][2]][st_ld[ii][3]]--;
                                 }
/*
                               for(ii=0;ii<6;ii++)
                                 {
                                   snd_dens[snd_ld[ii][0]][snd_ld[ii][1]][snd_ld[ii][2]][snd_ld[ii][3]]--;
                                 }
*/
                               vb[0]=vc[0];
                               vb[1]=vc[1];
                               vb[2]=vc[2];
                               ii=nn;
                               v=v-2;
                            }
                          else
                            {
                              prob_low=prob_high;
                              prob_high=prob_high+(12-loc_dens[st_ld[ii+1][0]][st_ld[ii+1][1]][st_ld[ii+1][2]][st_ld[ii+1][3]]);
/*
                              prob_high=prob_high+(6-snd_dens[st_ld[ii+1][0]][st_ld[ii+1][1]][st_ld[ii+1][2]][st_ld[ii+1][3]]);
*/
                            }
                        }
                    }
                }
            }
        }
    }
}

static void write_file(void)
{
  int i,j,k;
  int atom_1,atom_2,atom_3,atom_4;
  int count;
  double a[3],xx[3];
/* 
  fprintf(fq,"TITLE=\"DATA FILE\"\n");
  fprintf(fq,"VARIABLES=\"ID\" \"CHAIN\" \"X\" \"Y\" \"Z\"\n");
  fprintf(fq,"ZONE F=POINT\n");
*/
  printf("entered\n");
  fprintf(fq,"# Model for PE\n");
  fprintf(fq,"\n");
  fprintf(fq,"%10d     atoms\n",natom);
  fprintf(fq,"%10d     bonds\n",natom-n_chains);
  fprintf(fq,"%10d     angles\n",natom-2*n_chains);
  fprintf(fq,"%10d     dihedrals\n",natom-3*n_chains);
  fprintf(fq,"\n");
  fprintf(fq,"%10d     atom types\n",1);
  fprintf(fq,"%10d     bond types\n",1);
  fprintf(fq,"%10d     angle types\n",1);
  fprintf(fq,"%10d     dihedral types\n",1);
  fprintf(fq,"\n");
  fprintf(fq,"%10.4f%10.4f xlo xhi\n",0.0,(double)n_incs*lat);
  fprintf(fq,"%10.4f%10.4f ylo yhi\n",0.0,(double)n_incs*lat);
  fprintf(fq,"%10.4f%10.4f zlo zhi\n",0.0,(double)n_incs*lat);
  fprintf(fq,"\n");
  fprintf(fq,"Masses\n");
  fprintf(fq,"\n");
  fprintf(fq,"%10d %14.2f\n",1,mass);
  fprintf(fq,"\n");
  fprintf(fq,"Atoms\n");
  fprintf(fq,"\n");
 
  for(i=0;i<natom;i++)
    {
      xx[0]=(double)atom_list[i].x[0];
      xx[1]=(double)atom_list[i].x[1];
      xx[2]=(double)atom_list[i].x[2];
      if(atom_list[i].spot==0)
        {
          a[0]=0; 
          a[1]=0; 
          a[2]=0; 
        }
      else if(atom_list[i].spot==1)
        {
          a[0]=.5; 
          a[1]=.5; 
          a[2]=0; 
        }
      else if(atom_list[i].spot==2)
        {
          a[0]=.5; 
          a[1]=0; 
          a[2]=.5; 
        }
      else if(atom_list[i].spot==3)
        {
          a[0]=0; 
          a[1]=.5; 
          a[2]=.5; 
        }
      for(j=0;j<3;j++)
        {
          xx[j]=lat*(xx[j]+a[j]);
        }
      fprintf(fq,"%10d%10d%10d%10.4f%10.4f%10.4f\n",i+1,atom_list[i].chain,atom_list[i].type,xx[0],xx[1],xx[2]);
    }
  fprintf(fq,"\n");
  fprintf(fq,"Bonds \n");
  fprintf(fq,"\n");
  count=1;
  atom_1=1;
  atom_2=2;
  for(i=0;i<n_chains;i++)
    {
      for(j=0;j<c_length-1;j++)
        {
          fprintf(fq,"%10d%10d%10d%10d\n",count,1,atom_1,atom_2);
          count++;
          atom_1++;
          atom_2++;
        }
      atom_1++;
      atom_2++;
    }
  fprintf(fq,"\n");
  fprintf(fq,"Angles \n");
  fprintf(fq,"\n");
  count=1;
  atom_1=1;
  atom_2=2;
  atom_3=3;
  for(i=0;i<n_chains;i++)
    {
      for(j=0;j<c_length-2;j++)
        {
          fprintf(fq,"%10d%10d%10d%10d%10d\n",count,1,atom_1,atom_2,atom_3);
          count++;
          atom_1++;
          atom_2++;
          atom_3++;
        }
      atom_1=atom_1+2;
      atom_2=atom_2+2;
      atom_3=atom_3+2;
    }
  fprintf(fq,"\n");
  fprintf(fq,"Dihedrals \n");
  fprintf(fq,"\n");
  count=1;
  atom_1=1;
  atom_2=2;
  atom_3=3;
  atom_4=4;
  for(i=0;i<n_chains;i++)
    {
      for(j=0;j<c_length-3;j++)
        {
          fprintf(fq,"%10d%10d%10d%10d%10d%10d\n",count,1,atom_1,atom_2,atom_3,atom_4);
          count++;
          atom_1++;
          atom_2++;
          atom_3++;
          atom_4++;
        }
      atom_1=atom_1+3;
      atom_2=atom_2+3;
      atom_3=atom_3+3;
      atom_4=atom_4+3;
    }
}

  