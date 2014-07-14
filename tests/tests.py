#encoding:utf-8

""" unit tests.
Data required for these tests is the example project my_project mentioned in the tutorial.

"""

import inspect
import copy
import unittest
import os
import numpy as np
import spacegrids as sg


# test the info function

class TestInfo(unittest.TestCase):

  def setUp(self):
    print 'Setting up %s'%type(self).__name__

    self.fixture = sg.info_dict()

  def tearDown(self):
    print 'Tearing down %s'%type(self).__name__
    del self.fixture

  def test_type(self):
    
    self.assertEqual(type(self.fixture),dict)

  def test_type2(self):
    D = self.fixture
    if len(D) > 0:
      self.assertEqual(type(D.keys()[0]),str)

  def test_paths_in_D_exist(self):
    D = self.fixture
    for path in D.values():
      self.assertEqual(os.path.exists(path), True)  

class Test_project_helpers(unittest.TestCase):

  def setUp(self):
    print 'Setting up %s'%type(self).__name__
    D = sg.info_dict()
    self.fixture = D

  def tearDown(self):
    print 'Tearing down %s'%type(self).__name__
    del self.fixture



  def test_isexpdir_on_project_dir(self):

    D = self.fixture
    self.assertEqual(set(sg.isexpdir(os.path.join(D['my_project']))),  set(['DPO', 'DPC','Lev.cdf'] ) ) 


  def test_isexpdir_on_exper_dir(self):

    D = self.fixture
    self.assertEqual(sg.isexpdir(os.path.join(D['my_project'], 'DPO')),  ['time_mean.nc'] ) 


class TestCoordsOnTheirOwn(unittest.TestCase):

  def setUp(self):
    print 'Setting up %s'%type(self).__name__

    def provide_axis(cstack):
      for i, c in enumerate(cstack):
        cstack[i].axis = cstack[i].direction 

      return cstack
  
    # Note that some coord values are deliberately unordered.   

    # Coords ---    
    coord1 = sg.fieldcls.Coord(name = 'test1',direction ='X',value =np.array([1.,2.,3.]) , metadata = {'hi':5} )
    coord2 = sg.fieldcls.Coord(name = 'test2',direction ='Y',value =np.array([1.,2.,3.,4.]), metadata = {'hi':7})
    coord3 = sg.fieldcls.Coord(name = 'test',direction ='X',value =np.array([5.,1.,2.,3.,4.]), metadata = {'hi':3})
    # identical in main attributes to previous set (in order):
    coord4 = sg.fieldcls.Coord(name = 'test1',direction ='X',value =np.array([1.,2.,3.]), metadata = {'hi':8})
    coord5 = sg.fieldcls.Coord(name = 'test2',direction ='Y',value =np.array([1,2,3, 4]), metadata = {'hi':10})
    coord6 = sg.fieldcls.Coord(name = 'test',direction ='X',value =np.array([5,1,2,3, 4]), metadata = {'hi':12})

    # YCoords ---

    ycoord1 = sg.fieldcls.YCoord(name = 'test1',direction ='X',value =np.array([1.,2.,3.]) , metadata = {'hi':5} )
    ycoord2 = sg.fieldcls.YCoord(name = 'test2',direction ='Y',value =np.array([1.,2.,3.,4.]), metadata = {'hi':7})
    ycoord3 = sg.fieldcls.YCoord(name = 'test',direction ='X',value =np.array([5.,1.,2.,3.,4.]), metadata = {'hi':3})
    # identical in main attributes to previous set (in order):
    ycoord4 = sg.fieldcls.YCoord(name = 'test1',direction ='X',value =np.array([1.,2.,3.]), metadata = {'hi':8})
    ycoord5 = sg.fieldcls.YCoord(name = 'test2',direction ='Y',value =np.array([1.,2.,3., 4.]), metadata = {'hi':10})
    ycoord6 = sg.fieldcls.YCoord(name = 'test',direction ='X',value =np.array([5.,1.,2.,3., 4.]), metadata = {'hi':12})



    # XCoords ---

    xcoord1 = sg.fieldcls.XCoord(name = 'test1',direction ='X',value =np.array([1.,2.,3.]) , metadata = {'hi':5} )
    xcoord2 = sg.fieldcls.XCoord(name = 'test2',direction ='Y',value =np.array([1.,2.,3.,4.]), metadata = {'hi':7})
    xcoord3 = sg.fieldcls.XCoord(name = 'test',direction ='X',value =np.array([5.,1.,2.,3.,4.]), metadata = {'hi':3})
    # identical in main attributes to previous set (in order):
    xcoord4 = sg.fieldcls.XCoord(name = 'test1',direction ='X',value =np.array([1.,2.,3.]), metadata = {'hi':8})
    xcoord5 = sg.fieldcls.XCoord(name = 'test2',direction ='Y',value =np.array([1.,2.,3., 4.]), metadata = {'hi':10})
    xcoord6 = sg.fieldcls.XCoord(name = 'test',direction ='X',value =np.array([5.,1.,2.,3., 4.]), metadata = {'hi':12})




    # we are testing for Coord, YCoord and XCoord 
    cstack1 = provide_axis([coord1,coord2,coord3])
    cstack2 = provide_axis([coord4,coord5,coord6])

    ycstack1 = provide_axis([ycoord1,ycoord2,ycoord3])
    ycstack2 = provide_axis([ycoord4,ycoord5,ycoord6])

    xcstack1 = provide_axis([xcoord1,xcoord2,xcoord3])
    xcstack2 = provide_axis([xcoord4,xcoord5,xcoord6])


    self.fixture = [cstack1, cstack2, ycstack1, ycstack2,xcstack1, xcstack2,]

  def tearDown(self):
    print 'Tearing down %s'%type(self).__name__
    del self.fixture

  def test_init_method(self):
    """Test the __init__ method of Coord
    """
    
    self.assertRaises(ValueError, sg.fieldcls.Coord, **{'name' : 'test1','direction' :'X','value': np.array([1.,2.,3.]) , 'metadata': {'hi':5}, 'strings': ['foo','bar'] })

  def test_get_item_method(self):
    """Test the __getitem__ method of Coord class for success, failure and raised error.
    """
    coord1 = self.fixture[0][0]

    self.assertEqual(coord1[1], 2.)


  def test_coord_array_equal_method(self):
    """Test the array_equal method of Coord class for success, failure and raised error.
    """
    coord1 = self.fixture[0][0]
    coord2 = self.fixture[0][1]
    coord4 = self.fixture[1][0]

    self.assertEqual(coord1.array_equal(coord2), False)
    self.assertEqual(coord1.array_equal(coord4), True)
    self.assertRaises(TypeError, coord1.array_equal, 5)

  def test_coord_init_attributes_assigned(self):
    """
    Test whether all passed are assigned to attributes as intended. This is easy to forget when adding new arguments.
    """

    pass

  def test_copy_arguments_are_same_to_init(self):
    """
    Test whether the Coord copy method takes the same arguments as the __init__ method, with the exception of the Boolean equiv, which is a switch to the copy method. Note that XCoord and YCoord define their own copy methods and need to be tested separately.
    """

    self.assertEqual(inspect.getargspec(sg.fieldcls.Coord.copy).args[:-1] , inspect.getargspec(sg.fieldcls.Coord.__init__).args  )

  def test_copy_arguments_are_same_to_init_YCoord(self):
    """
    Test whether the YCoord copy method takes the same arguments as the __init__ method, with the exception of the Boolean equiv, which is a switch to the copy method. Note that XCoord and YCoord define their own copy methods and need to be tested separately.
    """

    self.assertEqual(inspect.getargspec(sg.YCoord.copy).args[:-1] , inspect.getargspec(sg.YCoord.__init__).args  )

  def test_copy_arguments_are_same_to_init_XCoord(self):
    """
    Test whether the XCoord copy method takes the same arguments as the __init__ method, with the exception of the Boolean equiv, which is a switch to the copy method. Note that XCoord and YCoord define their own copy methods and need to be tested separately.
    """

    self.assertEqual(inspect.getargspec(sg.XCoord.copy).args[:-1] , inspect.getargspec(sg.XCoord.__init__).args  )

  # ---------- test block for Coord class ------

  def test_copy_method_yields_not_same_for_case_name(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is the same as the original (although a different object in memory) and differs in that specific attribute.

    """

    cstack1 = self.fixture[0]
    coord2 = cstack1[-2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(name = 'joep')

    self.assertEqual(coord3_copy.name, 'joep'  )

  def test_copy_method_yields_not_same_for_case_dual(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is the same as the original (although a different object in memory) and differs in that specific attribute.

 
    """

    cstack1 = self.fixture[0]
    coord2 = cstack1[-2]
    coord3 = cstack1[-1]
    Z = sg.Ax('Z')
   
    coord3_copy = coord3.copy(dual = coord2)

    test_args = {'name':'joep', 'value':np.array([1.,2.,3.]),'dual':coord2,'axis':Z,'direction':'Z','units':'cm','long_name':'this is a coordinate in the x direction','metadata':{'hi':0},'strings':['five','one','two','three','four']}
 

    for ta in test_args:
      value = test_args[ta]
      coord3_copy = coord3.copy(**{ta:value})

      coord_att = getattr(coord3_copy,ta)
      if isinstance(coord_att,np.ndarray):
        self.assertEqual(np.array_equal(coord_att, value), True  )
      else:
        self.assertEqual(coord_att, value  )





  def test_same_method_yields_same(self):
    """
    Test whether making a copy with no arguments passed to .copy method yields a Coord object that is the same (with respect to .same method) as the original (although a different object in memory). Also tested for other Coord objects from fixture and for hybrid axis attributes (one str, one Ax).
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord4 = self.fixture[1][0]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy()

    self.assertEqual(coord3.same(coord3_copy),True  )
    self.assertEqual(coord1.same(coord4),True  )

    coord4.axis = sg.fieldcls.Ax(coord4.axis)
    self.assertEqual(coord1.same(coord4),True  )
    self.assertEqual(coord4.same(coord1),True  )
    self.assertEqual(coord1.same(coord3),False  )

  def test_same_method_yields_not_same_for_case_array(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[0]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(value = np.array([5,6,7]))

    self.assertEqual(coord3.same(coord3_copy), False  )

  def test_same_method_yields_not_same_for_case_name(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[0]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(name = 'joep')

    self.assertEqual(coord3.same(coord3_copy), False  )

  def test_same_method_yields_not_same_for_case_axis(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[0]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(axis = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )

  def test_same_method_yields_not_same_for_case_direction(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[0]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(direction = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )


  def test_same_method_yields_not_same_for_case_direction(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[0]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(direction = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )


  def test_cast_method_no_args(self):
    """
    Test Coord cast method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
 
    F = coord1.cast()
  
    self.assertEqual(F.shape, (3,)  )

  def test_cast_method_2D_grid(self):
    """
    Test Coord cast method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]     
    coord3 = cstack1[-1]

    F = coord1.cast(coord1*coord2)
  
    self.assertEqual(F.shape, (3,4)  )
    self.assertEqual( np.array_equal( F.value[1,:], np.array([2,2,2,2]) ), True  )
    self.assertEqual( np.array_equal( F.value[:,1], np.array([1.,2.,3.]) ), True  )


  def test_make_equiv_method(self):
    """
    Test Coord make_equiv method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]     
    coord3 = cstack1[-1]

    coord1.make_equiv(coord2)
  
    self.assertEqual(coord2 in coord1.equivs, True  )

  def test_is_equiv_method_false(self):
    """
    Test Coord is_equiv method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]     
    coord3 = cstack1[-1]
  
    self.assertEqual(coord1.is_equiv(coord2),  False  )
 

  def test_is_equiv_method_true(self):
    """
    Test Coord is_equiv method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]     
    coord3 = cstack1[-1]

    coord1.make_equiv(coord2)
  
    self.assertEqual(coord1.is_equiv(coord2),  True  )
    self.assertEqual(coord2.is_equiv(coord1),  True  )


  def test_eq_in_method_false(self):
    """
    Test Coord eq_in method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]     
    coord3 = cstack1[-1]
 
    self.assertEqual(coord1.eq_in(coord2*coord3),  None  )

  def test_eq_in_method_true(self):
    """
    Test Coord eq_in method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]     
    coord3 = cstack1[-1]

    coord1.make_equiv(coord2)
  
    self.assertEqual(coord1.eq_in(coord2*coord3),  coord2  )


  def test_pow_method(self):
    """
    Test Coord __pow__ method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
  
    self.assertEqual(coord1**2,  sg.Gr((coord1,))  )

  def test_mul_method_non_equiv(self):
    """
    Test Coord __mul__ method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]
  
    self.assertEqual((coord1*coord2).shape(),  (3,4)  )

  def test_mul_method_equiv(self):
    """
    Test Coord __mul__ method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]
      
    coord1.make_equiv(coord2)

    self.assertEqual((coord1*coord2).shape(),  (3,)  )

  def test_roll_function_non_masked(self):
    """Test the sg roll function
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]

    K = coord1(coord1*coord2)
    R= sg.roll(K,coord=coord1,mask = False)
    
    self.assertEqual( np.array_equal( R[0,:],  np.array([3.,3.,3.,3.]) ), True  )
    self.assertEqual( np.array_equal( R[1,:],  np.array([1.,1.,1.,1.]) ), True  )
    # first coord in R.gr is replaced:
    self.assertEqual( R.gr[0] is coord1, False  )
    # second coord in R.gr is not replaced:
    self.assertEqual( R.gr[1] is coord2, True  )

    # test whether coord in R.gr is properly rolled:
    self.assertEqual( np.array_equal(R.gr[0].value , np.array( [3., 1., 2.] )  ) , True  )


  def test_roll_function_non_masked_keepgrid(self):
    """Test the sg roll function
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]

    K = coord1(coord1*coord2)
    R= sg.roll(K,coord=coord1,mask = False, keepgrid = True)
    
    # first coord in R.gr is not replaced:
    self.assertEqual( R.gr[0] is coord1, True  )
    # second coord in R.gr is not replaced:
    self.assertEqual( R.gr[1] is coord2, True  )


  def test_roll_function_masked(self):
    """Test the sg roll function
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]

    K = coord1(coord1*coord2)
    R= sg.roll(K,coord=coord1,mask = True)
    
    self.assertEqual( np.isnan( R[0,:] ).all() , True  )
    self.assertEqual( np.array_equal( R[1,:],  np.array([1.,1.,1.,1.]) ), True  )


  def test_coord_shift_method(self):
    """
    Test Coord coord_shift method.

    Need to check the nan's that show up as numbers in the exposed area.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]
     
    K = coord1(coord1*coord2) 
    R = coord1.coord_shift(K,1)

    self.assertEqual( np.isnan( R[0,:] ).all() , True  )
    self.assertEqual( np.array_equal( R[1,:],  np.array([1.,1.,1.,1.]) ), True  )

  def test_trans_method(self):
    """
    Test Coord trans method.
    """

    cstack1 = self.fixture[0]

    coord1 = cstack1[0]
    coord2 = cstack1[1]
     
    K = coord1(coord1*coord2) 
    R = coord1.trans(K)

    self.assertEqual( np.array_equal( R[1,:],  np.array([1.,1.,1.,1.]) ), True  )
    self.assertEqual( np.array_equal( R[2,:],  np.array([1.,1.,1.,1.]) ), True  )

    self.assertEqual( R.gr[0] is coord1   , True  )


# -------- test block for YCoord class ---------------

  def testY_copy_method_yields_not_same_for_case_name(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is the same as the original (although a different object in memory) and differs in that specific attribute.

    """

    cstack1 = self.fixture[2]
    coord2 = cstack1[-2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(name = 'joep')

    self.assertEqual(coord3_copy.name, 'joep'  )

  def testY_copy_method_yields_not_same_for_case_dual(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is the same as the original (although a different object in memory) and differs in that specific attribute.

 
    """

    cstack1 = self.fixture[2]
    coord2 = cstack1[-2]
    coord3 = cstack1[-1]
    Z = sg.Ax('Z')
   
    coord3_copy = coord3.copy(dual = coord2)

    test_args = {'name':'joep', 'value':np.array([1.,2.,3.]),'dual':coord2,'axis':Z,'direction':'Z','units':'cm','long_name':'this is a coordinate in the x direction','metadata':{'hi':0},'strings':['five','one','two','three','four']}
 

    for ta in test_args:
      value = test_args[ta]
      coord3_copy = coord3.copy(**{ta:value})

      coord_att = getattr(coord3_copy,ta)
      if isinstance(coord_att,np.ndarray):
        self.assertEqual(np.array_equal(coord_att, value), True  )
      else:
        self.assertEqual(coord_att, value  )





  def test_Ysame_method_yields_same(self):
    """
    Test whether making a copy with no arguments passed to .copy method yields a Coord object that is the same (with respect to .same method) as the original (although a different object in memory).
    """

    cstack1 = self.fixture[2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy()

    self.assertEqual(coord3.same(coord3_copy),True  )

  def testY_same_method_yields_not_same_for_case_array(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(value = np.array([5,6,7]))

    self.assertEqual(coord3.same(coord3_copy), False  )

  def testY_same_method_yields_not_same_for_case_name(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(name = 'joep')

    self.assertEqual(coord3.same(coord3_copy), False  )

  def testY_same_method_yields_not_same_for_case_axis(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(axis = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )

  def testY_same_method_yields_not_same_for_case_direction(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(direction = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )


  def testY_same_method_yields_not_same_for_case_direction(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(direction = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )





# -------- test block for XCoord class ---------------

  def testX_copy_method_yields_not_same_for_case_name(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is the same as the original (although a different object in memory) and differs in that specific attribute.

    """

    cstack1 = self.fixture[4]
    coord2 = cstack1[-2]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(name = 'joep')

    self.assertEqual(coord3_copy.name, 'joep'  )

  def testX_copy_method_yields_not_same_for_case_dual(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is the same as the original (although a different object in memory) and differs in that specific attribute.

 
    """

    cstack1 = self.fixture[4]
    coord2 = cstack1[-2]
    coord3 = cstack1[-1]
    Z = sg.Ax('Z')
   
    coord3_copy = coord3.copy(dual = coord2)

    test_args = {'name':'joep', 'value':np.array([1.,2.,3.]),'dual':coord2,'axis':Z,'direction':'Z','units':'cm','long_name':'this is a coordinate in the x direction','metadata':{'hi':0},'strings':['five','one','two','three','four']}
 

    for ta in test_args:
      value = test_args[ta]
      coord3_copy = coord3.copy(**{ta:value})

      coord_att = getattr(coord3_copy,ta)
      if isinstance(coord_att,np.ndarray):
        self.assertEqual(np.array_equal(coord_att, value), True  )
      else:
        self.assertEqual(coord_att, value  )





  def test_Ysame_method_yields_same(self):
    """
    Test whether making a copy with no arguments passed to .copy method yields a Coord object that is the same (with respect to .same method) as the original (although a different object in memory).
    """

    cstack1 = self.fixture[4]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy()

    self.assertEqual(coord3.same(coord3_copy),True  )

  def testX_same_method_yields_not_same_for_case_array(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[4]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(value = np.array([5,6,7]))

    self.assertEqual(coord3.same(coord3_copy), False  )

  def testX_same_method_yields_not_same_for_case_name(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[4]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(name = 'joep')

    self.assertEqual(coord3.same(coord3_copy), False  )

  def testX_same_method_yields_not_same_for_case_axis(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[4]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(axis = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )

  def testX_same_method_yields_not_same_for_case_direction(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[4]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(direction = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )


  def testX_same_method_yields_not_same_for_case_direction(self):
    """
    Test whether making a copy with 1 argument passed to .copy method yields a Coord object that is NOT the same (with respect to .same method) as the original (and a different object in memory).

    Note that in general, the .same method tests for:

    self.array_equal(other)
    self.name == other.name
    self.axis == other.axis
    self.direction == other.direction 

    """

    cstack1 = self.fixture[4]
    coord3 = cstack1[-1]
   
    coord3_copy = coord3.copy(direction = 'Z')

    self.assertEqual(coord3.same(coord3_copy), False  )












# -----------------------



  def test_sort(self):
    cstack1 = self.fixture[0]
    coord3 = cstack1[-1]
    coord3.sort()
    value = copy.deepcopy(coord3.value)
    value.sort()
    self.assertEqual(coord3.value.any() , value.any()  )

  def test_equality_relation_weaksame(self):
    """"
    Does the &-relationship yield equality?
    """
    cstack1 = self.fixture[0]
    cstack2 = self.fixture[1]

    # First two coord objects should have same content

    self.assertEqual(cstack1[0].weaksame(cstack2[0]), True)

  def test_inequality_relation_weaksame(self):
    """"
    Does the &-relationship yield inequality?
    """

    cstack1 = self.fixture[0]
    cstack2 = self.fixture[1]

    # These two coord objects are not the same

    self.assertEqual(cstack1[0].weaksame(cstack2[1]), False)

  def test_equality_relation_find_equal_axes(self):
    """"
    Does the function find_equal_axes recognise equivalent coord objects in the two cstacks and replace the elements of the 2nd stack accordingly?
    """

    cstack1 = self.fixture[0]
    cstack2 = self.fixture[1]

    # this should remove all redundant coord objects with respect to &-equality
    sg.find_equal_axes(cstack1,cstack2)

    self.assertEqual(cstack1,cstack2)

  def test_make_axes_function_type_output(self):
    """
    The output should be a list of Ax objects ([X,Y] expected, see below)
    """

    cstack1 = self.fixture[0]
    cstack2 = self.fixture[1]

    self.assertEqual(isinstance(sg.make_axes(cstack1 + cstack2)[0],sg.Ax ) , True   )


  def test_make_axes_function_output_expected(self):
    """
    The test coords contain only X and Y direction Ax objects
    """

    cstack1 = self.fixture[0]
    cstack2 = self.fixture[1]

    self.assertEqual(str( sg.make_axes(cstack1 + cstack2) ) , '[X, Y]'  )


  def test_make_axes_function_no_output_expected(self):
    """
    Calling make_axes twice should not yield further output
    """

    cstack1 = self.fixture[0]
    cstack2 = self.fixture[1]
    sg.make_axes(cstack1 + cstack2) 
    self.assertEqual(str( sg.make_axes(cstack1 + cstack2) ) , '[]'  )



class TestUtilsg(unittest.TestCase):

  def test_id_index_id_in_rem_equivs_functions(self):
    """Test id_index, id_in and rem_equivs from sg.utilsg.
    """

    # set up some axes to test on:
    a1 = sg.fieldcls.Ax(name='a1')
    a2 = sg.fieldcls.Ax(name='a2')
    a3 = sg.fieldcls.Ax(name='a3')
    a4 = sg.fieldcls.Ax(name='a4')

    # b2 is equivalent to a2, b3 to none.
    b2 = sg.fieldcls.Ax(name='a2', direction ='Q', display_name='Q')
    b3 = sg.fieldcls.Ax(name='b3', direction ='Q', display_name='Q')
 
    # the tests
    self.assertEqual(sg.utilsg.id_in([a1,a2,a3,a4],b2  ) , True)
    self.assertEqual(sg.utilsg.id_in([a1,a2,a3,a4],b3  ) , False)   

    self.assertEqual(sg.utilsg.id_index([a1,a2,a3,a4],b2  ) , 1)
    self.assertEqual(sg.utilsg.id_index([a1,a2,a3,a4],b3  ) , None)
    self.assertEqual(sg.utilsg.rem_equivs([a1,a2,a3]+[b2,] ),  [a1, a2, a3] )

  def test_get_att_function(self):
    """Tests sg.utilsg.get_att
    """

    # define some test class with some attributes
    class Tmp(object):
      test =0
      test2=20
      test3=30

    W = Tmp()
    self.assertEqual(sg.utilsg.get_att(W,['test','test2'] ), 0 )
    self.assertEqual(sg.utilsg.get_att(W,['test2','test'] ), 20 )
    self.assertEqual(sg.utilsg.get_att(W,['test100'] ), None )


  def test_merge_function(self):
     """
     Tests whether 2 test arrays are properly merged.
     """

     # two test arrays to merge
     A = np.array([1.,2.,3.,4.])
     B = np.array([-10.,1.5,2.5,3.5,4.5,11.])

     self.assertEqual(sg.utilsg.merge(A,B).any(), np.array([-10. ,   1. ,   1.5,   2. ,   2.5,   3. ,   3.5,   4. ,   4.5,  11. ]).any()   )


# 3 tests for very simple function sublist in utilsg.py
# --------------
  def test_sublist(self):

    self.assertEqual(sg.utilsg.sublist(['test','hi'] ,'hi' ) , ['hi'])
     
  def test_sublist_all(self):

    self.assertEqual(sg.utilsg.sublist(['test','hi'] ,'*' ) , ['test','hi'])

  def test_sublist_none(self):

    self.assertEqual(sg.utilsg.sublist(['test','hi'] ,'ho' ) , [])


# -------------

  def test_add_alias(self):
    """
    Create some test coords to test the add_alias function in utilsg.py.

    An alias attribute is assigned, which is the same as the name attribute unless the name appears more than once.
    Two names are the same in this example, and in the created alias, the second of those two names must receive a suffix "2". 
    """
    coord1 = sg.fieldcls.Coord(name = 'test',direction ='X',value =np.array([1.,2.,3.]) , metadata = {'hi':5} )
    coord2 = sg.fieldcls.Coord(name = 'test',direction ='Y',value =np.array([1.,2.,3.,4.]), metadata = {'hi':7})

    coord3 = sg.fieldcls.Coord(name = 'test3',direction ='X',value =np.array([5.,1.,2.,3.,4.]), metadata = {'hi':3})

    coord4 = sg.fieldcls.Coord(name = 'test4',direction ='X',value =np.array([5.,1.,2.,3.,4.]), metadata = {'hi':5})

    L = sg.utilsg.add_alias([coord1, coord2, coord3, coord4])

    # test that alias is correct (same as names, but if the same name occurs >1 times, it is numbered)
    self.assertEqual([it.alias for it in L]  , ['test', 'test2', 'test3', 'test4'] )

    # test that names remain the same
    self.assertEqual([it.name for it in L]  , ['test', 'test', 'test3', 'test4'] )

  def test_find_perm_function_equal_length_permutables(self):
    """
    Test whether the permutation between two permutable lists yields the right result.
    """
    left = ['a','b','c']
    right = ['c','a','b']

    perm = sg.utilsg.find_perm(left,right)

    self.assertEqual([left[i] for i in perm] , right)

  def test_find_perm_function_non_equal_length(self):
    """
    Test whether the permutation between two non-permutable lists yields the right result.
    """
    left = ['a','b','c']
    right = ['c','a']

    perm = sg.utilsg.find_perm(left,right)

    self.assertEqual(perm, None)

  def test_find_perm_function_equal_length_non_permutables(self):
    """
    Test whether the permutation between two permutable lists yields the right result.
    """

    a=sg.fieldcls.Coord('a')

    b=sg.fieldcls.Coord('b')

    c=sg.fieldcls.Coord('c')

    left = [a,b]
    right = [b,c]

    perm = sg.utilsg.find_perm(left,right)

    self.assertEqual(perm, None)



  def test_simple_glob_function_left_wildcard(self):

    self.assertEqual(sg.utilsg.simple_glob(['foo','bar'],'*oo'  ), ['foo'] )

  def test_simple_glob_function_right_wildcard(self):

    self.assertEqual(sg.utilsg.simple_glob(['foo','bar'],'oo*'  ), ['foo'] )

  def test_simple_glob_function_right_wildcard(self):

    self.assertEqual(sg.utilsg.simple_glob(['foo','bar','vroom'],'*oo*'  ), ['foo','vroom'] )

  def test_simple_glob_function_no_wildcard(self):

    self.assertEqual(sg.utilsg.simple_glob(['foo','bar','vroom'],'oo'  ), [] )

  def test_end_of_filepath_function(self):

    self.assertEqual(sg.utilsg.end_of_filepath('/test/foo/bar'), 'bar')
    self.assertEqual(sg.utilsg.end_of_filepath('/foo/bar/'), 'bar')
    self.assertEqual(sg.utilsg.end_of_filepath('foo/bar/'), 'bar')

class TestExper(unittest.TestCase):

  def setUp(self):
    print 'Setting up %s'%type(self).__name__
    D = sg.info_dict()
    P = sg.Project(D['my_project']);
    #P.load('O_temp')
    self.fixture = P

  def tearDown(self):
    print 'Tearing down %s'%type(self).__name__
    del self.fixture


  def test_load_method_non_existent_var(self):
    P = self.fixture
    E = P['DPO']
    varname = 'this_doesnt_exist'

    # attempt to load non-existent field    
    P.load(varname)
    
    self.assertEqual(len(E.vars),0)


  def test_load_method_existent_var(self):
    P = self.fixture
    E = P['DPO']
    varname = 'O_temp'

    # attempt to load non-existent field    
    P.load(varname)
    
    self.assertEqual(len(E.vars),1)

  def test_load_method_multiple_existent_var(self):
    P = self.fixture
    E = P['DPO']
    varnames = ['A_sat', 'A_slat' ]

    # attempt to load non-existent field    
    P.load(varnames)
    
    self.assertEqual(len(E.vars),2)


  def test_get_function_of_Exper_not_loaded(self):
    # try to get a Field that has not been loaded yet from the Exper object => None returned.
    E = self.fixture['DPO']
   
    self.assertEqual(E.get('O_temp'),None)

  def test_get_of_Exper(self):
    # try to get a Field that has been loaded from the Exper object => Field object.
    E = self.fixture['DPO']
    self.fixture.load('O_temp')
    self.assertEqual(str(E.get('O_temp')), 'O_temp')

  def test_delvar_method_of_Exper(self):  

    # try to delete a Field that has been loaded from the Exper object 

    E = self.fixture['DPO']
    self.fixture.load(['O_temp','O_sal','A_sat','A_shum'])
    E.delvar('O_temp')
    self.assertEqual(E.get('O_temp') is None, True)

    E.delvar(['O_sal','A_sat'])
    self.assertEqual(E.get('O_sal') is None, True)
    self.assertEqual(E.get('A_sat') is None, True)

    del E['A_shum']
    self.assertEqual(E.get('A_shum') is None, True)

# tests around coord and grid aspects of fields

class TestCoordField(unittest.TestCase):

  def setUp(self):
    print 'Setting up %s'%type(self).__name__
    D = sg.info_dict()
    P = sg.Project(D['my_project']);P.load('O_temp')
    self.fixture = P

  def tearDown(self):
    print 'Tearing down %s'%type(self).__name__
    del self.fixture


  def test_field_grid_len(self):

    self.assertEqual(len(self.fixture['DPO']['O_temp'].gr),3)

  def test_field_shape(self):

    self.assertEqual(self.fixture['DPO']['O_temp'].shape,self.fixture['DPO']['O_temp'].gr.shape())

  def test_coord(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'

    self.assertEqual( latitude*(longitude*latitude) , longitude*latitude )

  def test_coord_mult2(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'

    self.assertEqual( latitude_edges*(longitude*latitude) , longitude*latitude_edges )
    

    
  def test_coord_div(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'

    self.assertEqual( (longitude*latitude)/longitude , latitude**2 )

   

  def test_coord_dual(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'

    self.assertEqual( longitude.dual, longitude_edges )
   
  def test_coord_mul_field(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'

    self.assertEqual( (longitude*self.fixture['DPO']['O_temp']).shape, (19,100) )

  def test_coord_div_field(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'

    self.assertEqual( (self.fixture['DPO']['O_temp'] / longitude).shape, (19,100) )

  def test_coord_2D_div_field(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'

    self.assertEqual( (self.fixture['DPO']['O_temp'] / (longitude*latitude ) ).shape, (19,) )


  def test_ax_mul_field(self):
    
    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'

    self.assertEqual( (X*self.fixture['DPO']['O_temp']  ).shape, (19, 100) )


  def test_can_I_divide_field_by_ax_shape(self):
    
    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'

    self.assertEqual( (self.fixture['DPO']['O_temp'] / X ).shape, (19, 100) )

  def test_can_I_divide_field_by_ax2D_shape(self):
    
    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'

    self.assertEqual( (self.fixture['DPO']['O_temp'] / (X*Y ) ).shape, (19,) )


  def test_avg_temp_value(self):

    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'

    self.assertAlmostEqual( self.fixture['DPO']['O_temp']/ (X*Y*Z) ,  3.9464440090035104 , places =2)


  def test_avg_temp_value_after_regrid(self):

    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'

    # load velocity to get the velocity grid
    self.fixture.load('O_velX')

    TEMP_regrid = self.fixture['DPO']['O_temp'].regrid(self.fixture['DPO']['O_velX'].gr)

    self.assertAlmostEqual( TEMP_regrid/ (X*Y*Z) , 4.092108709111132  , places =2)



  def test_squeezed_dims_worked_on_loading(self):

    self.assertEqual( len(self.fixture['DPO']['O_temp'].squeezed_dims) , 1   )

  def test_if_unsqueezing_adds_dims(self):

    self.assertEqual( len( (sg.unsqueeze(self.fixture['DPO']['O_temp']) ).gr ) , 4   )

  def test_if_unsqueezing_removes_squeezed_dims(self):

    self.assertEqual( len( (sg.unsqueeze(self.fixture['DPO']['O_temp']) ).squeezed_dims ) , 0   )


class TestFieldBasic(unittest.TestCase):

  def setUp(self):
    print 'Setting up %s'%type(self).__name__
    D = sg.info_dict()
    P = sg.Project(D['my_project']);
    P.load(['O_temp','A_sat'])
    self.fixture = P

  def tearDown(self):
    print 'Tearing down %s'%type(self).__name__
    del self.fixture

  def test_slice(self):

    SAT = self.fixture['DPO']['A_sat']

    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'       

    SAT_sliced = SAT[Y,:50]

    self.assertEqual( SAT_sliced.shape ,  (50,100)  )

  def test_cat(self):

    SAT = self.fixture['DPO']['A_sat']

    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'       

    SAT1 = SAT[Y,:40]
    SAT2 = SAT[Y,40:55]
    SAT3 = SAT[Y,55:]

    SAT_combined = sg.concatenate((SAT1,SAT2,SAT3))

    self.assertEqual( SAT_combined.shape ,  (100,100)  )




class TestGrid(unittest.TestCase):

  def setUp(self):
    print 'Setting up %s'%type(self).__name__
    D = sg.info_dict()
    P = sg.Project(D['my_project']);
    P.load(['O_temp','A_sat'])
    self.fixture = P

  def tearDown(self):
    print 'Tearing down %s'%type(self).__name__
    del self.fixture



  def test_inflate(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    Igr = (depth*latitude*longitude).inflate()

    self.assertEqual(Igr[0].shape, (19, 100, 100))


  def test_grid_permute_function_equal_len_and_coords(self):

# Corresponds to CASE 1a in equal length grid case in fieldcls.py source code.
    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth*longitude
    gr2 = longitude*depth

    # define a np array consistent with gr1
    A = np.ones( gr1.shape()  )

    # gr1(gr2) should yield a function transposing ndarrays consistent with gr1 to ndarrays consistent with gr2

    self.assertEqual((gr1(gr2)(A)).shape, gr2.shape() )

  def test_grid_permute_function_equal_len_equiv_coords_only(self):

# Corresponds to CASE 1b in equal length grid case in fieldcls.py source code.

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

   # This time, we are going to a new grid that requires interpolation (on longitude).
 
    gr1 = depth*longitude
    gr2 = longitude_V*depth

    # define a np array consistent with gr1
    A = np.ones( gr1.shape()  )

    # gr1(gr2) should yield a function transposing ndarrays consistent with gr1 to ndarrays consistent with gr2, and interpolated onto it.

    self.assertEqual((gr1(gr2)(A)).shape, gr2.shape() )

  def test_grid_permute_function_equal_len_equiv_coords_only(self):

# Corresponds to CASE 1c in equal length grid case in fieldcls.py source code.

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

   # This time, we are going to a new grid that is incompatible, leading to a None result.
 
    gr1 = depth*longitude
    gr2 = latitude*depth

    self.assertEqual(gr1(gr2), None )


  def test_gr_method_expand_size(self):
    """
    Test expand method of fieldcls.py


    SAT = P['DPO']['A_sat']
    SAT.shape is (100,100)
    W=SAT.gr.expand(SAT[:],depth**2)
    W.shape is (19,100,100)
    W contains 19 identical copies (slices) of SAT[:] 

    """

    SAT = self.fixture['DPO']['A_sat']

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   
    
    W=SAT.gr.expand(SAT[:],depth**2)

#    W has been expanded, and the other grid (depth**2) should be appended on the left side.         

    self.assertEqual(W.shape, (19,100,100)  )

  def test_gr_method_expand_broadcast(self):
    """
    Test expand method of fieldcls.py
    """

    SAT = self.fixture['DPO']['A_sat']

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   
    
    W=SAT.gr.expand(SAT[:],depth**2)

#    W contains 19 identical copies (slices) of SAT[:]          

    K=W[:,50,50]
    self.assertEqual((K == K[0]).all() , True  )

  def test_call_small_gr_on_big_gr(self):

    SAT = self.fixture['DPO']['A_sat']

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'   

    # need to do slice test earlier.
    SAT2 = SAT[Y,:50]

    gr1 = SAT2.gr
    gr2 = depth*SAT2.gr

    A = SAT2[:]
    B = gr1(gr2)(A)

    self.assertEqual(B.shape ,  (19, 50, 100) )

  def test_call_small_gr_on_big_gr_permute(self):

    """
    corresponds to case 2a of gr class call method in fieldcls.py
    """

    SAT = self.fixture['DPO']['A_sat']

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'   

    # need to do slice test earlier.
    SAT2 = SAT[Y,:50]

    gr1 = SAT2.gr
    # note that this does something different for a single coord left multiplicant:
    gr2 = (depth*longitude)*SAT2.gr   

    A = SAT2[:]
    B = gr1(gr2)(A)

    self.assertEqual(B.shape ,  (19, 100, 50) )

  def test_call_small_gr_on_big_gr_permute_interp(self):

    """
    corresponds to case 2b of gr class call method in fieldcls.py
    """


    SAT = self.fixture['DPO']['A_sat']

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    for c in self.fixture['DPO'].axes:
      exec c.name + ' = c'   

    # need to do slice test earlier.
    SAT2 = SAT[Y,:50]

    gr1 = SAT2.gr
    # note that this does something different for a single coord left multiplicant:
    gr2 = (depth*longitude_V)*SAT2.gr   

    A = SAT2[:]
    B = gr1(gr2)(A)

    self.assertEqual(B.shape ,  (19, 100, 50) )
    
  def test_call_small_gr_on_big_gr_not_equiv(self):

    """
    corresponds to case 2c of gr class call method in fieldcls.py
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   


    self.assertEqual(depth(latitude*longitude) ,  None )


  def test_gr_method_reduce_dim1vs3_len_list(self):
    """
    Test reduce method of gr class
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth**2
    gr2 = depth*latitude*longitude

    A = np.ones(gr2.shape() )

    # should have the length of len(depth)
    self.assertEqual(len(gr1.to_slices(A,gr2)) ,  19 )
    
  def test_gr_method_reduce_dim1vs3_shape_element(self):
    """
    Test reduce method of gr class
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth**2
    gr2 = depth*latitude*longitude

    A = np.ones(gr2.shape() )

    # should have the shape of latitude*longitude
    self.assertEqual( gr1.to_slices(A,gr2)[0].shape  ,  (100,100) )

  def test_gr_method_reduce_dim2vs3_len_list(self):
    """
    Test reduce method of gr class
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth*latitude
    gr2 = depth*latitude*longitude

    A = np.ones(gr2.shape() )

    # should have the length of len(depth)*len(longitude) 
    self.assertEqual(len(gr1.to_slices(A,gr2)) ,  1900 )
    
  def test_gr_method_to_slices_dim2vs3_shape_element(self):
    """
    Test to_slices method of gr class
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth*latitude
    gr2 = depth*latitude*longitude

    A = np.ones(gr2.shape() )

    # should have the shape of longitude**2
    self.assertEqual( gr1.to_slices(A,gr2)[0].shape  ,  (100,) )

  def test_gr_method_vsum(self):

    """
    Test vsum method of gr class
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth*latitude

    # should have the shape of longitude**2
    self.assertAlmostEqual( gr1.vsum(gr1.ones() )  , 121672626836.47124 , places =2 )


  def test_gr_method_find_args_coord(self):

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    ctypes = {'x_coord':sg.XCoord,'y_coord':sg.YCoord,'z_coord':sg.fieldcls.Coord}
  
    self.assertEqual((latitude*longitude).find_args_coord(coord_types = ctypes) , 
    [[], [latitude]] )

    
  def test_gr_method_der_type(self):

    """
    Test der method of gr class to see whether it returns a Field
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = longitude*latitude

    # should have the shape of longitude**2
    self.assertEqual( isinstance( gr1.der(longitude,gr1.ones() ) , sg.Field )  , True )

  def test_gr_method_der_X(self):

    """
    Test der method of gr class to see whether it returns a Field
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = longitude*latitude

    W = gr1.der(longitude,gr1.ones() )

    W.value[np.isnan(W.value)]=1

    # should have the shape of longitude**2
    self.assertEqual( W.value.sum()   , 0.0 )

  def test_gr_method_der_Y(self):

    """
    Test der method of gr class to see whether it returns a Field
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth*latitude

    W = gr1.der(latitude,gr1.ones() )

    W.value[np.isnan(W.value)]=1

    # should have the shape of longitude**2
    self.assertEqual( W.value.sum()   , 19.0 )

  def test_gr_method_vol(self):

    """
    Test volume method 
    """

    for c in self.fixture['DPO'].cstack:
      exec c.name + ' = c'   

    gr1 = depth*latitude

    W = gr1.vol()
    # should have the shape of longitude**2
    self.assertAlmostEqual( W.value.sum()   , 121672626836.47124 , places = 2 )



# --------- run the classes ------------

if __name__ == '__main__':
    unittest.main()

