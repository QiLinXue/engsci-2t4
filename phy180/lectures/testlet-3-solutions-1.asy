if(!settings.multipleView) settings.batchView=false;
settings.tex="pdflatex";
settings.inlinetex=true;
deletepreamble();
defaultfilename="testlet-3-solutions-1";
if(settings.render < 0) settings.render=4;
settings.outformat="";
settings.inlineimage=true;
settings.embed=true;
settings.toolbar=false;
viewportmargin=(2,2);

import graph; size(8cm);
real labelscalefactor = 0.5; /* changes label-to-point distance */
pen dps = linewidth(0.7) + fontsize(10); defaultpen(dps); /* default pen style */
pen dotstyle = black; /* point style */
real xmin = -9.873849401848743, xmax = 10.34597482922314, ymin = -4.902471408686772, ymax = 5.6951996247039745; /* image dimensions */

/* draw figures */
draw((6,-2)--(-4,3));
draw((6,-2)--(4,-2));
draw((0,1)--(0,-1),EndArrow(6));
draw((0,-1)--(-4,-1),EndArrow(6));
draw((0,1)--(1.5,4),EndArrow(6));
draw((1.5,4)--(4,3),EndArrow(6));
draw((-4,-1)--(4,3), linetype("2 2"));
label("$\mu N$",(2.5713932900829275,4.150167457286181),SE*labelscalefactor);
label("$N$",(0.2065015671505436,2.819915863136715),SE*labelscalefactor);
label("$mg$",(0.1030375542722518,0.17419324810611054),SE*labelscalefactor);
label("$ma$",(-2.261854168660132,-0.6969360529700459),SE*labelscalefactor);
draw(shift((6,-2))*xscale(1.2728588954640063)*yscale(1.2728588954640063)*arc((0,0),1,153.434948822922,180));
draw(shift((0,1))*xscale(0.8368516664389005)*yscale(0.8368516664389005)*arc((0,0),1,26.565051177077983,63.43494882292201));
draw(shift((0,1))*xscale(0.4983831431667102)*yscale(0.4983831431667102)*arc((0,0),1,206.565051177078,270));
label("$\alpha$",(4.389403802087198,-1.4812309579465584),SE*labelscalefactor);
label("$\theta$",(0.590796472127056,2.162642613573726),SE*labelscalefactor);
label("$\beta$",(-0.5620882428024813,0.5437075798142956),SE*labelscalefactor);
/* dots and labels */

clip((xmin,ymin)--(xmin,ymax)--(xmax,ymax)--(xmax,ymin)--cycle);
