/* figproc.c */
#include <stdio.h>
#include <ctype.h>

#define ERROR -1

int getinteger(int base);
int header(int base);


int main(void)
{
	unsigned int ch,bit;
    unsigned int luminosity,grey;
    int magic_number=0;
    unsigned int red,blue,green;
    unsigned int max_val,color;
    int i,j,height,width;
    
    /* these commands display the header of the file */
    putchar('P');
    while (magic_number==0)
    {
    	if (getchar()=='P')
    	{
    	    magic_number=getchar();
    	    putchar(magic_number-1);
    	    putchar('\n');	
		}
    }
	width=header(10);
    while (width==-1)
	    width=header(10);
	printf("%d",width);
    putchar(32);
	height=header(10);
	while (height==-1)
	    height=header(10);
	printf("%d",height);
	putchar('\n');
	max_val=header(10);
	while (max_val==-1)
	    max_val=header(10);
	if (magic_number=='3' || magic_number=='6') 
	{   
	    printf("%d",max_val);
	    putchar('\n');
	}
	if (magic_number=='3')
	{
		/* converts a ppm (P3) to pgm (P2) file */
	    ch=getchar();
		while (ch!=EOF)
		{
			/* converts one color pixel at a time to grayscale until the input file is finished */
		   	ungetc(ch, stdin);
		    red=getinteger(10);
			green=getinteger(10);
			blue=getinteger(10);
			luminosity=(299*red+587*green+114*blue)/1000;
			printf("%d",luminosity);
			putchar(32);
			ch=getchar();
		}
	}
	else if (magic_number=='2')
	{
		/* converts a pgm (P2) to pbm (P1) file */
	    ch=getchar();
	    while (ch!=EOF)
	    {
	    	/* converts one grayscale pixel at the time to white-black untill the input file is finished */
	    	ungetc(ch, stdin);
	    	grey=getinteger(10);
	    	if (grey>(max_val+1)/2)
	    	{
	    	    putchar('0');
	    		putchar(32);
	    	}
	    	else
			{ 
	    		putchar('1');
	    		putchar(32);
	    	}
	    	ch=getchar();
		}
	}
	else if (magic_number=='6')
	{
		/* P6 (binary RGB) to P5 (binary grayscale).
		 * Read exactly three bytes per pixel, without skipping any bytes. */
		if (max_val > 255)
		{
			fprintf(stderr, "16-bit P6 samples are not supported\n");
			return 1;
		}
		for (j=0; j<height; j++)
		{
			for (i=0; i<width; i++)
			{
				int r=getchar();
				int g=getchar();
				int b=getchar();
				if (r==EOF || g==EOF || b==EOF)
				{
					fprintf(stderr, "Truncated P6 pixel data\n");
					return 1;
				}
				luminosity=(299u*(unsigned int)r+587u*(unsigned int)g+
				            114u*(unsigned int)b)/1000u;
				putchar((int)luminosity);
			}
		}
	}
	else if (magic_number=='5')
	{
		/* converts a pgm (P5) to pbm (P4) file */
		ch=getchar();
		while (ch!=EOF)
		{
			color=0;
			for (bit=0; bit<8; bit++) /* packs 8 pixels at a time */
			{
				color<<=1; /* raise the color with 0 for a white pixel */
				if (ch<=(max_val+1)/2)
					color|=1; /* raise the color with 1 for a black pixe; */
				ch=getchar();
				if (ch==EOF)
					break;
			}
			putchar(color);
			if (width%8!=0) /* in case the width is not a multiple of 8 add one bit */
			{
				color=0;
				for (i=0; i<width%8; i++)
				{
	                ch=getchar();
	                color<<=1;
	                if (ch<=(max_val+1)/2)
	                    color|=1;
				}
				color<<=8-width%8;
				putchar(color);
			}
		}
	}
}

int getinteger(int base) 
{
    char ch=getchar();
    int val=0; 
    while (ch==32 || ch==10 || ch==9)
    {
    	if (ch==10)
    	    putchar(ch);
    	ch=getchar();
    }
	while (ch!=32 && ch!=10 && ch!=9)    /* Read up to new line */
	{
        if (ch >= '0' && ch <= '0'+base-1)   /* Legal character? */
        {
		    val = base*val + (ch-'0');      /* Update return value */
            ch=getchar();
        }
        else
            return ERROR;                /* Illegal character read */
    }
    ungetc(ch, stdin);
    return val;
}

int header(int base)
{
    char ch=getchar(); // get only one char and save for later use
    int val=0; // 0 means not changed
    if (ch=='#')
    {
    	while (ch!='\n')
    	    ch=getchar();
	}
    while (ch>='0' && ch <= '0'+base-1) { // if "ch" is not a number, this loop will be skipped
            val=base*val+(ch-'0');
            ch=getchar(); // get a new char for next loop iteration and checking if it is digit
    }
    if (val==0) // val was not changed (ch was not a number)
        return ERROR; // loop in "main" will be continued
    else
        return val; // val was changed, return it
}
