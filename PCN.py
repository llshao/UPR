#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 15:39:00 2017

@author: Leilai Like Coding
"""
from bitstring import BitArray, BitStream
import copy
import gc
######!!!!!!!!!!!!!!!!Be careful about BitArray!!!!!!!!!!!!!!
############slicing returns BitArray obj even for x[1:2],; however indexing return BOOLEAN:Ture/False
############For Ex: b=BitArray('0b1100110011')
################# b[0]--True  b[0:1]--BitArray('0b1')
class PCN:
    def __init__(self):
        self.PCN_num=0
        self.Var_num=0   
        self.PCN_list=list()
        return None
#############################################################
##################Initialization functions###################
    def read_pcn(self,filename):
        handle = open(filename,'r')
        ## Read the file and parse it into PCN format
        temp=list()       
        for line in handle:
            temp.append(line)
        self.varInit(int(temp[0]),int(temp[1]))
        for line in temp[2:]:
            self.append(line)
        handle.close()
        del temp
        del handle
        gc.collect()
        return None
        
    def write_pcn(self,filename):
        handle = open(filename,'w')
        handle.write(str(self.Var_num))
        handle.write('\n')
        handle.write(str(self.PCN_num))
        handle.write('\n')
        ## Read the file and parse it into PCN format    
        for line in self.PCN_list:
            temp=str()  
            temp+=str(line[0])
            for index in range(self.Var_num):
                if not line[1][index*2:index*2+2]==BitArray('0b11'):
                    if  line[1][index*2:index*2+2]==BitArray('0b01'):
                        temp+=' '
                        temp+=str(index+1)
                    if  line[1][index*2:index*2+2]==BitArray('0b10'):
                        temp+=' '
                        temp+=str(-index-1)
            handle.write(temp+'\n')
        handle.close()
        del temp
        del handle
        gc.collect()
        return None
        
    def append(self,Line) :
        lineparsed=self.par(Line)
        self.PCN_list.append(lineparsed)
        return None
        
    def varInit(self,var,pcn) :
        self.Var_num=var
        self.PCN_num=pcn
        return None
        
    def par(self,Line) :
        linesplit=Line.split()
        Parsedl=BitArray('0b11')*self.Var_num## Initialize with all DONT CARE '11'
        for word in linesplit[1:]:
            if int(word)<0:
                Parsedl[2*(abs(int(word))-1):2*abs(int(word))]=0b10## Be careful [lb,up], where up is excluded
            else:
                Parsedl[2*(abs(int(word))-1):2*abs(int(word))]=0b01
        return [int(linesplit[0]),Parsedl]   

####################################################################
#######################Find the binate Variabel#####################
    def binateFind(self):       
        print('binateFind')
        T_C=self.TC_cal()        #Calculate the |T-C|
        UorNot=self.UnateJudge() #Judge Unate or NOT
        print('T_C',T_C)
        print('UorNot',UorNot)
#        print('DontCare',DontCareRes)
        if all(UorNot):## all unate
#            unate_index=[i for i, j in enumerate(DontCareRes) if j == False]
#            unate_TC=[T_C[i] for i in unate_index]
#            max_index=unate_TC.index(max(unate_TC))
            max_index=T_C.index(max(T_C))
            print('Unate Find',max_index)
            print(self.PCN_list)
            return max_index
        else:
            binate_index=[i for i, j in enumerate(UorNot) if j == False]
            binate_TC=[T_C[i] for i in binate_index]
            min_index=binate_TC.index(min(binate_TC))
            print('Binate find',binate_index,binate_index[min_index])
            print(self.PCN_list)
            return binate_index[min_index]
            
    def TC_cal(self) :
        tc=list([0])*self.Var_num
        for line in self.PCN_list:
            lstmp=line[1]
            #print(int(len(lstmp)/2))
            for index in range(self.Var_num): # range [0, 1, 2...] start from 0
                tc[index]=tc[index]+int(lstmp[2*index:2*index+2]==BitArray('0b01'))-int(lstmp[2*index:2*index+2]==BitArray('0b10'))
        tc_abs=[abs(number) for number in tc]
        return tc_abs
        
    def UnateJudge(self) :
        unateOrnot=BitArray('0b00')*self.Var_num
        DontCare=BitArray('0b11')*self.Var_num
        unateRes=list([True])*self.Var_num
#        DontCareRes=list([False])*self.Var_num
        for line in self.PCN_list:
            unateOrnot=unateOrnot|(~line[1])
            DontCare=DontCare & line[1]
        for index in range(self.Var_num):
            if unateOrnot[2*index:2*index+2]==BitArray('0b11'):
                unateRes[index]=False
#            if DontCare[2*index:2*index+2]==BitArray('0b11'):
#                DontCareRes[index]=True
        return unateRes
##########################################################################
        ############## Boolean Operation of the PCN lists##############
    def ANDX(self,Xindex):
#        print('ANDX')
#        print( self.PCN_list)
        for index in range(self.PCN_num):
            self.PCN_list[index][1][2*Xindex:2*Xindex+2]='0b01'
            self.PCN_list[index][0]+=1
#        print( self.PCN_list)
        return None
            
    def ANDXB(self,Xindex):
#        print('ANDXB')
#        print( self.PCN_list)
        for index in range(self.PCN_num):
            self.PCN_list[index][1][2*Xindex:2*Xindex+2]='0b10'
            self.PCN_list[index][0]+=1
#        print( self.PCN_list)
        return None
        
    def ORPN(self,P,N):
#        print('ORPN')
#        print(P.PCN_list)
#        print(N.PCN_list)
#        if P.PCN_list:
#            if (P.PCN_list[0][0]==0) | (P.PCN_list[0][1]==BitArray('0b11')*P.Var_num):
#                P.PCN_num=1
#                P.PCN_list=[[0,BitArray('0b11')*P.Var_num]]
#                return(P)  
#        if N.PCN_list:
#            if (N.PCN_list[0][0]==0) | (N.PCN_list[0][1]==BitArray('0b11')*P.Var_num):
#                P.PCN_num=1
#                P.PCN_list=[[0,BitArray('0b11')*P.Var_num]]
#                return(P)  
        P.PCN_num+=N.PCN_num
        P.PCN_list+=N.PCN_list
        self.PCN_num=P.PCN_num
        self.PCN_list=P.PCN_list
#        print(P.PCN_list)
        return None
#################################################################################
###################### PCN return determination #####################################        
    def PCN_CHECK(self):
#        print('Check')
        if self.PCN_num<=1:
            if self.PCN_num==0:
                self.PCN_list=[[0,BitArray('0b11')*self.Var_num]]## Return the complemented results
                self.PCN_num=1
#                print(self.PCN_list)
#                print('End Check')
                return True ## indicate it is simple enough to return
            if self.PCN_list[0][0]==0:
                self.PCN_list=list()
                self.PCN_num=0
#                print(self.PCN_list)
#                print('End Check')
                return True
            temp=list()
            temp_num=0
            for index in range(self.Var_num):
                ls_tem=BitArray('0b11')*self.Var_num;
                if not (self.PCN_list[0][1][2*index:2*index+2]==BitArray('0b11')):
                    ls_tem[2*index:2*index+2]=~self.PCN_list[0][1][2*index:2*index+2]
                    temp.append([1,ls_tem])
                    temp_num+=1
            self.PCN_list=temp
            self.PCN_num=temp_num
#            print(self.PCN_list)
#            print('End Check')
            return True 
                        
        else:
            if self.PCN_list[0][1]==self.PCN_list[1][1]:## remove redundant
                del self.PCN_list[1]
                self.PCN_num-=1
            for line in self.PCN_list:
                if line[0]==0:
                    self.PCN_list=list()
                    self.PCN_num=0
    #                print(self.PCN_list)
    #                print('End Check')
                    return True 
            print(self.PCN_list)
            print('End Check')
            return False ## indicate it is still too complex
#############################################################
###################### P/NCofactor ##########################
    def PCofactor(self, Xindex):
#        print('Pcofactor')
        temp=PCN()
        temp.PCN_num=self.PCN_num
        temp.Var_num=self.Var_num
        print(self.PCN_list)
        for line in self.PCN_list:
            if line[1][Xindex*2+1:2*Xindex+2]==BitArray('0b1'):##0b01 or 0b11
                temp_line=copy.deepcopy(line)
                temp_line[0]-=int(line[1][Xindex*2:2*Xindex+1]==BitArray('0b0'))## if it is '0b01' -1
                temp_line[1][Xindex*2:2*Xindex+1]='0b1'
                print('Is same?',temp_line==line)
                if temp_line[0]==0:## find 1
                    temp.PCN_num=1
                    temp.PCN_list=[[0,BitArray('0b11')*self.Var_num]]
#                    print(temp.PCN_list)
#                    print('END Pfactor, PCN#',temp.PCN_num)
                    return temp
                temp.PCN_list.append(temp_line)
            else:
                temp.PCN_num-=1
#                print('PCN_num',self.PCN_num,temp.PCN_num)
#        print(temp.PCN_list)
#        print('END Pfactor, PCN#',temp.PCN_num)
        return temp
        
    def NCofactor(self, Xindex):
#        print('Ncofactor')
        temp=PCN()
        temp.PCN_num=self.PCN_num
        temp.Var_num=self.Var_num
        print(self.PCN_list)
        for line in self.PCN_list:
            if line[1][Xindex*2:2*Xindex+1]==BitArray('0b1'):##0b10 or 0b11
                temp_line=copy.deepcopy(line)
                temp_line[0]-=int(line[1][Xindex*2+1:2*Xindex+2]==BitArray('0b0'))## if it is '0b10' -1
                temp_line[1][Xindex*2+1:2*Xindex+2]='0b1'
                if temp_line[0]==0:## find 1
                    temp.PCN_num=1
                    temp.PCN_list=[[0,BitArray('0b11')*self.Var_num]]
#                    print(temp.PCN_list)
#                    print('END Nfactor, PCN#', temp.PCN_num)
                    return temp
                temp.PCN_list.append(temp_line)
            else:
                temp.PCN_num-=1
#        print(temp.PCN_list)
#        print('END Nfactor, PCN#', temp.PCN_num)
        return temp
#################################################
                ##### Complment ######
    def Complement(self):
        gc.enable()
#        print('Comp')
        if self.PCN_CHECK():
            print('End Comp',self.PCN_list)
            gc.collect()
            return None
        else:
            binate_index=self.binateFind()
            print('Binate_index',binate_index)
            Pfactor=self.PCofactor(binate_index)
            print('Pfactor',Pfactor.PCN_list)
            Pfactor.Complement()
            print('Binate_index',binate_index)
            Nfactor=self.NCofactor(binate_index)
            print('Nfactor',Nfactor.PCN_list)
            Nfactor.Complement()
            Pfactor.ANDX(binate_index)
            Nfactor.ANDXB(binate_index)
            self.ORPN(Pfactor,Nfactor)
            print('Pfactor',Pfactor.PCN_list)
            print('Nfactor',Nfactor.PCN_list)
            print(self.PCN_list)
            del Pfactor
            del Nfactor
            gc.collect()
            return None