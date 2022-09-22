from queue import PriorityQueue
class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn

        # You should keep updating following variable with best string so far.
        self.best_state = None  
        self.my_matrix ={}


    ######################## function to convert the confusion Matrix

    def convert_conf(self):
        l1=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for ab in l1:
            self.my_matrix[ab]=[]
        for ij in l1:
            for ab in self.conf_matrix[ij]:
                self.my_matrix[ab].append(ij)


    ######################## Replacing the best character in the i'th index of current state


    def best_replacement_for_character(self,current_state,index):
        curr_cost=self.cost_fn(current_state)
        curr_list = list(current_state)
        new_state_cost = curr_cost
        new_state =current_state
        curr_char =curr_list[index]
        ##########
        
        for a in self.my_matrix[curr_list[index]]:
            curr_list[index] = a
            temp_new_state ="".join(curr_list)
            ########################
            if(self.cost_fn(temp_new_state) < new_state_cost):
                new_state_cost = self.cost_fn(temp_new_state)
                new_state = temp_new_state
            curr_list[index]=curr_char
            ############
        if(new_state_cost < curr_cost):
            return new_state
        return current_state
    

    ######################################### getting the k best successors of a state
    

    def get_k_states(self,current_state,k,length_of_state):
        list_of_k_states=[]
        P_q = PriorityQueue()
            #############
        l1 =list(current_state)
        for i in range(length_of_state):

            if(l1[i] == ' ' ):
                continue
            else:
                temp_state = self.best_replacement_for_character(current_state,i)
                temp_cost = self.cost_fn(temp_state)
                P_q.put((temp_cost,temp_state))           
            ##################################
        q_z = P_q.qsize()-k
        count =0
        ff = 0
        for i in range(k):
            #appending pair of cost and state_string
            item = P_q.get()
            if(i!=0 and count < q_z):
                if(item[0]>ff):
                    list_of_k_states.append(item)
                else:
                    continue
            else:
                list_of_k_states.append(item)
            count=count+1
            ff =item[0]
            

        # del P_q
        return list_of_k_states
     
    ##################### getting the next best k seccessors
    def get_best_k_successors(self,state_list,k):
        Successor_list=[]
        P_q = PriorityQueue()
        for l1 in state_list:
            for state in l1:
                P_q.put(state)
        ############
        q_z = P_q.qsize()-k
        count =0
        ff = 0
        
        for i in range(k):
            my_pair = P_q.get()
            ########appending only state string
            if(i!=0 and count < q_z):
                if(my_pair[0]>ff):
                    Successor_list.append(my_pair[1])
                    
                else:
                    continue

            else:
                Successor_list.append(my_pair[1])
            count=count+1
            ff =my_pair[0]

        # del P_q
        return Successor_list


############################################


    def search(self, start_state):
        
        self.convert_conf()
        # print(self.my_matrix)
        str_st_len =len(start_state)
        ####
        k = str_st_len // 5
        if(k > 6):
            k=6
        ########
        l1 =self.get_k_states(start_state,k,str_st_len)
        My_Successors = self.get_best_k_successors([l1],k)
        itr = 8           #####################
        while(itr > 0):
            temp_list =[]
            for i in range(k):
                temp_list.append(self.get_k_states(My_Successors[i],k,str_st_len))
            My_Successors=self.get_best_k_successors(temp_list,k)
            # print(itr)
            itr=itr-1
            # del temp_list
            #########################
        self.best_state=My_Successors[0]
        return self.best_state
        """
        :param start_state: str Input string with spelling errors
        """
        # You should keep updating self.best_state with best string so far.
        # self.best_state = start_state
        