/* figproc.c */
#include <stdio.h>
#include <ctype.h>
#include <limits.h>

#define ERROR -1

int getinteger(int base);
int header(int base);


int main(void)
{
	int ch;
    unsigned int luminosity;
    int grey;
    int magic_number=0;
    unsigned int red,blue,green;
    int max_val;
    unsigned int color;
    int i,j,height,width;
    
    /* Validate the input header before writing any output. */
    if (getchar()!='P')
    {
        fprintf(stderr, "Invalid Netpbm magic number\n");
        return 1;
    }
    magic_number=getchar();
    if (magic_number!='2' && magic_number!='3' &&
        magic_number!='5' && magic_number!='6')
    {
        fprintf(stderr, "Unsupported Netpbm format\n");
        return 1;
    }
    width=header(10);
    height=header(10);
    max_val=header(10);
    if (width<=0 || height<=0 || max_val<=0 || max_val>65535)
    {
        fprintf(stderr, "Invalid or incomplete Netpbm header\n");
        return 1;
    }
    if ((magic_number=='5' || magic_number=='6') && max_val>255)
    {
        fprintf(stderr, "16-bit binary samples are not supported\n");
        return 1;
    }
    putchar('P');
    putchar(magic_number-1);
    putchar('\n');
    printf("%d %d\n",width,height);
    if (magic_number=='3' || magic_number=='6')
    {
        printf("%d\n",max_val);
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
		/* P5 (8-bit grayscale) to P4 (packed binary bitmap).
		 * Each row starts at a new byte; unused low bits are zero. */
		if (max_val > 255)
		{
			fprintf(stderr, "16-bit P5 samples are not supported\n");
			return 1;
		}
		for (j=0; j<height; j++)
		{
			color=0;
			for (i=0; i<width; i++)
			{
				int sample=getchar();
				if (sample==EOF)
				{
					fprintf(stderr, "Truncated P5 pixel data\n");
					return 1;
				}
				color=(color<<1) | (sample<=(max_val+1)/2 ? 1u : 0u);
				if (i%8==7)
				{
					putchar((int)color);
					color=0;
				}
			}
			if (width%8!=0)
					putchar((int)(color << (8-width%8)));
		}
	}
}

/* Parse an unsigned decimal token with whitespace and # comment support.
 * Return ERROR on malformed input, EOF, or integer overflow. */
int header(int base)
{
    int ch;
    int val=0;
    int digits=0;
    if (base!=10)
        return ERROR;
    for (;;)
    {
        ch=getchar();
        if (ch==EOF)
            return ERROR;
        if (ch=='#')
        {
            do { ch=getchar(); } while (ch!=EOF && ch!='\n');
            if (ch==EOF)
                return ERROR;
            continue;
        }
        if (isspace((unsigned char)ch))
            continue;
        break;
    }
    while (ch>='0' && ch<='9')
    {
        int digit=ch-'0';
        if (val>(INT_MAX-digit)/10)
            return ERROR;
        val=val*10+digit;
        digits++;
        ch=getchar();
    }
    if (!digits)
        return ERROR;
    if (ch!=EOF && !isspace((unsigned char)ch))
        return ERROR;
    return val;
}

int getinteger(int base)
{
    return header(base);
}
