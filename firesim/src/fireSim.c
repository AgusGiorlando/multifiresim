////////////////////// ESTE CODIGO HA SIDO MODIFICADO  ////////////////////////
//
// Autor (modif) German Bianchini y Miguel Méndez-Garabetti
// Fecha:	 22/03/2018
//
// Modificaciones al codigo orig:
// 				-El "modelNumber" era de tipo size_t.
// 				-Algunas nuevas variables para poder efectuar
// 				la creacion de un nuevo modelo con su respectiva
// 				particula.
// 				-Otras variables (cant, countm, countp) para con-
// 				trolar bucles durante la impresion de valores de
// 				modelos y sus particulas.
// 				-Se ha comentado el codigo de impresion del
// 				mapa de altura del fuego.
// 				
// IMPORTANTE: ahora es necesario pasar por argumento al programa:
// 	
// 				(1) fichero_salida
// 				(2) modelo
// 				(3) slope
// 				(4) mapa entrada (para puntos de ignicion)
// 				(5) valor inicial para definir area de ignicion
// 				(6) valor final (tiempo) para la simulacion
// Ej.
//   ./fireSim test 7 21 513-58-50.map 0.5 4.6
// 				 
// IMPORTANTE:  la impresion del mapa ha sido impresa en el orden correcto, pues
// 		en el codigo original se imprime de la ultima fila hasta la
//		primera. 
//		
//////////////////////////////////////////////////////////////////////////////
/* 
 *******************************************************************************
 *
 *  fireSim.c
 *
 *  Description
 *      A very simple fire growth simulator to demonstrate the fireLib library.
 *
 *  Notice
 *      THIS IS FOR ILLUSTRATIVE PURPOSES ONLY, AND IS NOT AN ACCURATE FIRE
 *      GROWTH MODEL!!  THE 8-NEIGHBOR CELL CONTAGION ALGORITHM RESULTS IN
 *      SIGNIFICANT GEOMETRIC FIRE SHAPE DISTORTION AT SLIGHT ANGLES FROM
 *      45 DEGREES!
 *
 *  Legalities
 *      Copyright (c) 1996 Collin D. Bevins.
 *      See the file "license.txt" for information on usage and redistribution
 *      of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 *
 *  Try the Following Modifications
 *      Change the Rows, Cols, CellWd or CellHt to change map size & resolution.
 *      Fill the fuelMap[] array with heterogenous and/or discontinuous fuels.
 *      Put some NoFuel (0) breaks into fuelMap[] for the fire to spread around.
 *      Fill the slpMap[] and aspMap[] arrays with variable terrain.
 *      Fill the wspdMap[] and wdirMap[] arrays with variable wind.
 *      Fill the m***Map[] arrays with variable fuel moistures.
 *******************************************************************************
 */

#include "fireLib.h"

#define INFINITY 999999999.     /* or close enough */
#define PI 3.14159265
/* NOTE 1: Change these to modify map size & resolution. */
int    Rows   = 121;     /* Number of rows in each map.  Se recibe por parametro */
int    Cols   = 91;     /* Number of columns in each map. Se recibe por parametro */
double CellWd = 3.28;    /* Cell width (E-W) in feet. Donde 1 feet = 30.45 cm.  Se recibe por parametro*/
double CellHt = 3.28;    /* Cell height (N-S) in feet. */

/* NOTE 2: Change these to set uniform burning conditions. */
//static int Model   = 14;     /* Nuevo modelo definido con carga 0.6kg/m2 en base al modelo 8,9 y 10 */
static int Model = 7;		/* Se recibe por parametro */
//static double WindSpd = 11.855;     /* mph */
static double WindSpd = 0.0;//3.97;//6.487;     /* mph */
//static double WindDir = 251.86;     /* degrees clockwise from north */
static double WindDir = 0.0;//33.8;     /* degrees clockwise from north */
static double Slope   = 0.0;	/* fraction rise / reach -- equivale a tangente(alfa)-- TAN(PI*alfa/180)* Por parametro*/
static double Aspect  = 180.0;    /* degrees clockwise from north */
static double M1      = 0.15;//0.113;    /* 1-hr dead fuel moisture */
static double M10     = 0.22;//0.113;    /* 10-hr dead fuel moisture */
static double M100    = 0.35;//0.113;    /* 100-hr dead fuel moisture */
static double Mherb   = 0.3;//1.77952;   /* Live herbaceous fuel moisture */
static double Mwood   = 1.50;   /* Live woody fuel moisture */
//////////////////// AGREGADO POR GERMAN ///////////////////////
int xx, yy, leer, dato_int;
float dato;
int cant, countm, countp; /* contador para particulas*/
float inicial;
float endtime;
FILE *ficherocell, *modelfile; /* Aque se recibe el mapa de entrada que define el area de ignicion en conjunto con "valor"*/
////////////////////////////////////////////////////////////////
static int PrintMap _ANSI_ARGS_((double *map, char *fileName ));

int main ( int argc, char **argv )
{
  /////////////////////// AGREGADO POR GERMAN //////////////////////////////
  int x_ini;
  if (argc != 7)
    {
	    printf ("******************************************************************************\n");
	    printf ("  FORMATO DE LA LLAMADA*\n\n");
	    printf ("  fireSim <file-salida> <#modelo> <slope> <file-ign> <time-inicio> <time-end>\n");
	    printf ("******************************************************************************\n");
	    exit(1);
    }
    // La linea siguiente ha sido agregada para leer los parametros e imprimir
    Model = atoi(argv[2]);
    Slope = tan(PI*(atoi(argv[3]))/180);
    inicial = atof(argv[5]);
    endtime = atof(argv[6]);
    //Open del archivo de celdas (contiene las dimensiones y las celdas iniciales)
    if ((ficherocell=fopen(argv[4],"r+t"))==NULL)
    {
        //Error al abrir el archivo de celdas
        printf("No se puede abrir el archivo de celdas: %s\n", argv[4]);
        exit(1);
    }
    ///Leer las dimensiones (X e Y) y el tamaño de las celdas (CellWd y CellHt)
    fscanf(ficherocell,"#%*s %d %d %lf %lf\n",&Cols,&Rows,&CellWd,&CellHt);
    printf("-----------------------------------------------------------------\n");
    printf("\tPARAMETROS RECIBIDOS\n\n");
    printf("\t <mapa salida>\t\t %s\n",argv[1]);
    printf("\t <modelo>\t\t %d\n",Model);
    printf("\t <slope>\t\t %f\n",Slope);
    printf("\t <mapa entrada>\t\t %s\n",argv[4]);
    printf("\t <limite inicial>\t %1.2f\n",inicial);
    printf("\t <limite final>\t\t %1.2f\n",endtime);
    printf("\t <Cols>\t\t\t %d\n",Cols);
    printf("\t <Rows>\t\t\t %d\n",Rows);
    printf("\t <CellWd>\t\t %1.3f\n",CellWd);
    printf("\t <CellHt>\t\t %1.3f\n",CellHt);
    printf("-----------------------------------------------------------------\n");
  //////////////////////////////////////////////////////////////////////////  	
    /* neighbor's address*/     /* N  NE   E  SE   S  SW   W  NW */
    static int nCol[8] =        {  0,  1,  1,  1,  0, -1, -1, -1};
    static int nRow[8] =        {  1,  1,  0, -1, -1, -1,  0,  1};
    static int nTimes = 0;      /* counter for number of time steps */
    FuelCatalogPtr catalog;     /* fuel catalog handle */
    //////////////////////// AGREGADO POR GERMAN //////////////////////
    FuelModelPtr model;		/* fuel model handle*/
    FuelParticlePtr particles;	/* fuel particle handle*/
    //////////////////////////////////////////////////////////////////
    double nDist[8];            /* distance to each neighbor */
    double nAzm[8];             /* compass azimuth to each neighbor (0=N) */
    double timeNow;             /* current time (minutes) */
    double timeNext;            /* time of next cell ignition (minutes) */
    int    row, col, cell;      /* row, col, and index of current cell */
    int    nrow, ncol, ncell;   /* row, col, and index of neighbor cell */
    int    n, cells;            /* neighbor index, total number of map cells */
    int modelNumber;  /*aca*/       /* fuel model number at current cell */
    double moisture[6];         /* fuel moisture content at current cell */
    double fpm;                 /* spread rate in direction of neighbor */
    double minutes;             /* time to spread from cell to neighbor */
    double ignTime;             /* time neighbor is ignited by current cell */
    int    atEdge;              /* flag indicating fire has reached edge */
    int *fuelMap;    /*aca*/        /* ptr to fuel model map */
    double *ignMap;             /* ptr to ignition time map (minutes) */
    double *flMap;              /* ptr to flame length map (feet) */
    double *slpMap;             /* ptr to slope map (rise/reach) */
    double *aspMap;             /* ptr to aspect map (degrees from north) */
    double *wspdMap;            /* ptr to wind speed map (ft/min) */
    double *wdirMap;            /* ptr to wind direction map (deg from north) */
    double *m1Map;              /* ptr to 1-hr dead fuel moisture map */
    double *m10Map;             /* ptr to 10-hr dead fuel moisture map */
    double *m100Map;            /* ptr to 100-hr dead fuel moisture map */
    double *mherbMap;           /* ptr to live herbaceous fuel moisture map */
    double *mwoodMap;           /* ptr to live stem fuel moisture map */

    /* NOTE 3: allocate all the maps. */
    cells = Rows * Cols;
    if ( (ignMap   = (double *) calloc(cells, sizeof(double))) == NULL
      || (flMap    = (double *) calloc(cells, sizeof(double))) == NULL
      || (slpMap   = (double *) calloc(cells, sizeof(double))) == NULL
      || (aspMap   = (double *) calloc(cells, sizeof(double))) == NULL
      || (wspdMap  = (double *) calloc(cells, sizeof(double))) == NULL
      || (wdirMap  = (double *) calloc(cells, sizeof(double))) == NULL
      || (m1Map    = (double *) calloc(cells, sizeof(double))) == NULL
      || (m10Map   = (double *) calloc(cells, sizeof(double))) == NULL
      || (m100Map  = (double *) calloc(cells, sizeof(double))) == NULL
      || (mherbMap = (double *) calloc(cells, sizeof(double))) == NULL
      || (mwoodMap = (double *) calloc(cells, sizeof(double))) == NULL
      || (fuelMap  = (int *) calloc(cells, sizeof(int))) == NULL )/*aca los cast*/
    {
        fprintf(stderr, "Unable to allocate maps with %d cols and %d rows.\n",
            Cols, Rows);
        return (1);
    }

    
    /* NOTE 4: initialize all the maps -- modify them as you please. */
    for ( cell=0; cell<cells; cell++ )
    {
	/////////////////////////////////////////////////////////////////////
	fuelMap[cell]  = Model;
        slpMap[cell]   = Slope;
        aspMap[cell]   = Aspect;
        wspdMap[cell]  = 88. * WindSpd;     /* convert mph into ft/min */
        wdirMap[cell]  = WindDir;
        m1Map[cell]    = M1;
        m10Map[cell]   = M10;
        m100Map[cell]  = M100;
        mherbMap[cell] = Mherb;
        mwoodMap[cell] = Mwood;
        ignMap[cell]   = INFINITY;
        flMap[cell]    = 0.;
    }

/////////////////// INCORPORACION DE LA LECTURA DEL MAPA DE MODELOS /////////////////////

   // Open del archivo de modelos
   // Se guarda en un arreglo (ModelMap) para enviar a los workers
   if ((modelfile=fopen("ModelMap.in","r"))==NULL)
   {
        //Error al abrir el archivo
        printf("No se puede abrir el archivo de modelos: %s\n", "ModelMap.in");
        printf("Se usara el modelo indicado por linea de comandos (%d)\n", Model);
        //exit(1);
   }
   else
   {//Leer el archivo de entrada ModelMap.in
        for (yy=0; yy<Rows; yy++)
        {
             for (xx=0; xx<Cols; xx++)
             {  
                 leer=fscanf(modelfile,"%d",&dato_int);
                 fuelMap[xx+(yy*Cols)]=dato_int;
             }
        }
        fclose(modelfile);
        printf("Se usara el mapa de modelos %s\n", "ModelMap.in");
   }
///////////////////////////////////////////////////////////////////////////////////////



    /* NOTE 5: set an ignition time & pattern (this ignites the middle cell). */
    //////////////// Agregado por German ////////////////////////////////////////
    
/////////////////////////////////////////////////////////////////////////////////	
	///Completar el mapa de ignicion con las celdas quemadas
	for (yy=0; yy<Rows; yy++)
	{	
         for (xx=0; xx<Cols; xx++)
	  {
	     fscanf(ficherocell,"%f",&dato);
	     if (dato <= inicial && dato !=0) 
		ignMap[xx+(yy*Cols)]=inicial;//1.0;
	  }
	}
	fclose(ficherocell);
    /////////////////////////////////////////////////////////////////////////////////

    /*cell = Cols/3 + Cols*(Rows/4);*/
    /*cell = 2*Cols/3 + Cols*(Rows/4);*/
    //////////////////////////////////////////////////////////////////////////////////

    /* NOTE 6: create a standard fuel model catalog and a flame length table. */
    catalog = Fire_FuelCatalogCreateStandard("Standard", 13);
    
    /////////////////////////////// AGREGADO POR GERMAN /////////////////////////////
    ////// UTILIZADO PARA LA IMPRESION DE LOS VALORES DE LOS DISTINTOS MODELOS //////
    // Creacion de un nuevo modelo de fuego (el # 14)
    //Fire_FuelModelCreate(catalog,14,"NNFL14","gestosa con 1.967kg/m2",3.9,0.4,1,1);

    //Fire_FuelParticleAdd(catalog,14,FIRE_TYPE_DEAD,0.402873,1828.8,32,8000,0.0555,0.01);
    /*for(countm=1; countm<=14; countm++)
    {
     printf("Numero de modelo: %d\n",countm);
     printf("............modelNumber	%d\n", Fuel_Model(catalog,countm));
     printf("............*modelName	%s\n", Fuel_Name(catalog,countm));
     printf("............*desc		%s\n", Fuel_Desc(catalog,countm));
     printf("............depth		%g\n", Fuel_Depth(catalog,countm));
     printf("............mext		%g\n", Fuel_Mext(catalog,countm));
     printf("............adjust		%g\n", Fuel_SpreadAdjustment(catalog,countm));
     printf("............maxparticles	%d\n", Fuel_MaxParticles(catalog,countm));
     cant=Fuel_Particles(catalog, countm);
     printf("Cantidad de particulas %d\n",cant);
     for (countp=0; countp<cant; countp++)
     {
	    printf("Indice de particula: %d\n", countp);
 	    printf("................type %d\n", Fuel_Type(catalog,countm,countp));
	    printf("................load %g\n", Fuel_Load(catalog,countm,countp));
	    printf("................sarv %g\n", Fuel_Savr(catalog,countm,countp));
	    printf("................dens %g\n", Fuel_Density(catalog,countm,countp));
	    printf("................heat %g\n", Fuel_Heat(catalog,countm,countp));
	    printf("................stot %g\n", Fuel_SiTotal(catalog,countm,countp));
	    printf("................sef  %g\n", Fuel_SiEffective(catalog,countm,countp));
     }
     printf("###########################\n");
    }*/
    ///////////////////////////////////////////////////////////////////////////////////
    
    Fire_FlameLengthTable(catalog, 500, 0.1);

    /* Calculate distance across cell to each neighbor and its azimuth. */
    for ( n=0; n<8; n++ )
    {
        nDist[n] = sqrt ( nCol[n] * CellWd * nCol[n] * CellWd
                        + nRow[n] * CellHt * nRow[n] * CellHt );
        nAzm[n] = n * 45.;
    }

    /* NOTE 7: find the earliest (starting) ignition time. */
    for ( timeNext=INFINITY, cell=0; cell<cells; cell++ )
    {
        if ( ignMap[cell] < timeNext )
            timeNext = ignMap[cell];
    }

    /* NOTE 8: loop until no more cells can ignite or fire reaches an edge. */
    atEdge = 0;
    //while (timeNext < INFINITY && !atEdge))
    while ( timeNext < INFINITY && timeNext < endtime )
    {
        timeNow  = timeNext;
        timeNext = INFINITY;
        nTimes++;

        /* NOTE 9: examine each ignited cell in the fuel array. */
        for ( cell=0, row=0; row<Rows; row++ )
        {
            for ( col=0; col<Cols; col++, cell++ )
            {
                /* Skip this cell if it has not ignited. */
                if ( ignMap[cell] > timeNow )
                {
                    /* NOTE 12: first check if it is the next cell to ignite. */
                    if ( ignMap[cell] < timeNext )
                        timeNext = ignMap[cell];
                    continue;
                }
 
                /* NOTE 10: flag if the fire has reached the array edge. */
               if ( row==0 || row==Rows-1 || col==0 || col==Cols-1 )
                   atEdge = 1;

                /* NOTE 11: determine basic fire behavior within this cell. */
                modelNumber = fuelMap[cell];
                moisture[0] = m1Map[cell];
                moisture[1] = m10Map[cell];
                moisture[2] = m100Map[cell];
                moisture[3] = m100Map[cell];
                moisture[4] = mherbMap[cell];
                moisture[5] = mwoodMap[cell];
                Fire_SpreadNoWindNoSlope(catalog, modelNumber, moisture);
                Fire_SpreadWindSlopeMax(catalog, modelNumber, wspdMap[cell],
                    wdirMap[cell], slpMap[cell], aspMap[cell]);

                /* NOTE 12: examine each unignited neighbor. */
                for ( n=0; n<8; n++ )
                {
                    /* First find the neighbor's location. */
                    nrow = row + nRow[n];
                    ncol = col + nCol[n];
                    if ( nrow<0 || nrow>=Rows || ncol<0 || ncol>=Cols )
                        continue;
                    ncell = ncol + nrow*Cols;

                    /* Skip this neighbor if it is already ignited. */
                    if ( ignMap[ncell] <= timeNow )
                        continue;

                    /* Determine time to spread to this neighbor. */
                    Fire_SpreadAtAzimuth(catalog, modelNumber, nAzm[n], FIRE_NONE);
                    if ( (fpm = Fuel_SpreadAny(catalog, modelNumber)) > Smidgen)
                    {
                        minutes = nDist[n] / fpm;
	////////////// German: cambio de la condicion para controlar el tiempo de finalizacion ///////////////
                        /* Assign neighbor the earliest ignition time. */
                        if ( ((ignTime = timeNow + minutes)<ignMap[ncell])  && ((timeNow + minutes)<endtime) )
                        //if ( ((ignTime = timeNow + minutes)<ignMap[ncell])  )
                        {
                            ignMap[ncell] = ignTime;
                            Fire_FlameScorch(catalog, modelNumber, FIRE_FLAME);
                            flMap[ncell] = Fuel_FlameLength(catalog,modelNumber);
                        }

                        /* Keep track of next cell ignition time. */
                        if ( ignTime < timeNext )
                            timeNext = ignTime;
                    }
                }   /* next neighbor n */
            }   /* next source col */
        }   /* next source row */
    } /* next time */

    printf("There were %d time steps ending at %3.2f minutes (%3.2f hours).\n",
        nTimes, timeNow, timeNow/60.);

    /* NOTE 13: if requested, save the ignition & flame length maps. */
    if ( argc > 1 )
        PrintMap(ignMap, argv[1]);
    // La linea siguiente ha sido comentada para no imprimir el mapa de altura de fuego
    /*if ( argc > 2 )
        PrintMap(flMap, argv[2]);*/

    return (0);
}

static int PrintMap ( map, fileName )
    double *map;
    char   *fileName;
{
    FILE *fPtr;
    int cell, col, row;

    if ( (fPtr = fopen(fileName, "w")) == NULL )
    {
        printf("Unable to open output map \"%s\".\n", fileName);
        return (FIRE_STATUS_ERROR);
    }

    fprintf(fPtr,"#Dimensiones %d %d %1.3f %1.3f\n",Cols, Rows,CellWd,CellHt);
    //fprintf(fPtr, "Model: %d north: %1.0f\nsouth: %1.0f\neast: %1.0f\nwest: %1.0f\nrows: %d\ncols: %d\n",
    //    Model,(Rows*CellHt), 0., (Cols*CellWd), 0., Rows, Cols);
    // La linea siguiente ha sido comentada por German
    //    for ( row=Rows-1; row>=0; row-- )
    //    La linea siguiente ha sido agregada por German
    for ( row=0; row<Rows; row++ )
    {
        for ( cell=row*Cols, col=0; col<Cols; col++, cell++ )
        {
            //fprintf(fPtr, " %1.2f", (map[cell]==INFINITY) ? 0.0 : 1.0);
            fprintf(fPtr, " %1.2f", (map[cell]==INFINITY) ? 0.0 : map[cell]);
        }
        fprintf(fPtr, "\n");
    }
    fclose(fPtr);
    return (FIRE_STATUS_OK);
}
