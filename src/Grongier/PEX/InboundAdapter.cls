/* Copyright (c) 2021 by InterSystems Corporation.
   Cambridge, Massachusetts, U.S.A.  All rights reserved.
   Confidential property of InterSystems Corporation. */

Class Grongier.PEX.InboundAdapter Extends (Ens.InboundAdapter, Grongier.PEX.Common) [ Inheritance = right, ProcedureBlock, System = 4 ]
{

Parameter SETTINGS = "%classname:Python InboundAdapter,%module:Python InboundAdapter,%settings:Python InboundAdapter,%classpaths:Python InboundAdapter";

Method OnTask() As %Status
{
	set tSC = $$$OK
	try {
		$$$ThrowOnError(..Connect())
		$$$ThrowOnError(..%class."on_task"())
	} catch ex {
		set tSC = ex.AsStatus()
	}
	quit tSC
}

}
